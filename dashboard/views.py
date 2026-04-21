import json
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from .decorators import role_required
from .forms import AccountCreationForm, FrameCommentForm
from .models import ClinicianProfile, FrameComment, PatientAlert, PatientProfile, PressureFrame
from .utils import heatmap_cells

User = get_user_model()
INTERVAL_MAP = {'3h': 3, '9h': 9, '24h': 24}


def role_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect(
        'dashboard:admin_dashboard'
        if request.user.role == User.Roles.ADMIN
        else 'dashboard:clinician_dashboard'
        if request.user.role == User.Roles.CLINICIAN
        else 'dashboard:patient_dashboard'
    )


def _patient_sessions(patient):
    return patient.sessions.order_by('session_date')


def _filter_frames(patient, session_id=None, interval='24h'):
    sessions = _patient_sessions(patient)
    selected = sessions.filter(id=session_id).first() if session_id else sessions.last()
    if not selected:
        return sessions, None, PressureFrame.objects.none()
    hours = INTERVAL_MAP.get(interval, 24)
    end = selected.started_at + timedelta(hours=hours)
    return sessions, selected, selected.frames.filter(recorded_at__lt=end).order_by('recorded_at')


def _predict(frames):
    peak = max((f.peak_pressure_index for f in frames), default=0)
    base = [('A', 78, 'high risk', 10), ('B', 45, 'medium risk', 20), ('C', 23, 'low risk', 30)]
    out = []
    for name, prob, risk, time in base:
        out.append(
            {
                'region': f'Region {name}',
                'probability': max(8, min(99, round(prob + (peak - 100) / 5))),
                'risk': risk,
                'time': time,
            }
        )
    return out


@role_required(User.Roles.PATIENT)
def patient_dashboard(request):
    patient = get_object_or_404(
        PatientProfile.objects.select_related('user', 'clinician__user'), user=request.user
    )
    sessions, selected_session, frames_qs = _filter_frames(
        patient, request.GET.get('day'), request.GET.get('interval', '24h')
    )
    frames = list(frames_qs)
    selected_frame = frames[-1] if frames else None
    interval = request.GET.get('interval', '24h')
    chart_mode = request.GET.get('chart', 'interval')

    if request.method == 'POST' and selected_frame:
        form = FrameCommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.frame = selected_frame
            c.author = request.user
            c.save()
            messages.success(request, 'Comment submitted.')
            return redirect(f'{request.path}?day={selected_session.id}&interval={interval}')
    else:
        form = FrameCommentForm()

    latest_alert = (
        PatientAlert.objects.filter(patient=patient, reviewed=False)
        .select_related('frame')
        .first()
    )
    comments = (
        selected_frame.comments.filter(parent__isnull=True).select_related('author')
        if selected_frame
        else []
    )
    all_session_frames = list(selected_session.frames.order_by('recorded_at')) if selected_session else []
    hour_frames = []
    if selected_frame:
        start_hour = selected_frame.recorded_at - timedelta(hours=1)
        hour_frames = [f for f in all_session_frames if f.recorded_at >= start_hour]

    def _series(frame_list, attr):
        return [round(getattr(f, attr), 2) for f in frame_list]

    chart_sets = {
        'hour': {
            'labels': [f.recorded_at.strftime('%H:%M') for f in hour_frames],
            'ppi': _series(hour_frames, 'peak_pressure_index'),
            'contact': _series(hour_frames, 'contact_area_percent'),
        },
        'interval': {
            'labels': [f.recorded_at.strftime('%H:%M') for f in frames],
            'ppi': _series(frames, 'peak_pressure_index'),
            'contact': _series(frames, 'contact_area_percent'),
        },
        'day': {
            'labels': [f.recorded_at.strftime('%H:%M') for f in all_session_frames],
            'ppi': _series(all_session_frames, 'peak_pressure_index'),
            'contact': _series(all_session_frames, 'contact_area_percent'),
        },
    }
    if chart_mode not in chart_sets:
        chart_mode = 'interval'

    predictive = _predict(frames)
    return render(
        request,
        'dashboard/patient_dashboard.html',
        {
            'patient': patient,
            'sessions': sessions,
            'selected_session': selected_session,
            'interval': interval,
            'chart_mode': chart_mode,
            'selected_frame': selected_frame,
            'heatmap_cells': heatmap_cells(selected_frame.matrix_json) if selected_frame else [],
            'latest_alert': latest_alert,
            'current_metrics': {
                'peak_pressure_index': round(selected_frame.peak_pressure_index, 1) if selected_frame else 0,
                'contact_area_percent': round(selected_frame.contact_area_percent, 1) if selected_frame else 0,
                'average_pressure': round(selected_frame.average_pressure, 1) if selected_frame else 0,
                'reposition_per_hour': round(selected_frame.reposition_per_hour, 1) if selected_frame else 0,
                'high_pressure_time': sum(1 for f in frames if f.flagged_for_review),
            },
            'comment_form': form,
            'comments': comments,
            'chart_labels': json.dumps(chart_sets[chart_mode]['labels']),
            'ppi_data': json.dumps(chart_sets[chart_mode]['ppi']),
            'contact_area_data': json.dumps(chart_sets[chart_mode]['contact']),
            'predictive': predictive,
            'recommendation': predictive[0]['risk'] if predictive else 'low risk',
        },
    )


@role_required(User.Roles.PATIENT)
def dismiss_patient_alert(request, alert_id):
    alert = get_object_or_404(PatientAlert, id=alert_id, patient__user=request.user)
    if request.method == 'POST':
        alert.reviewed = True
        alert.save(update_fields=['reviewed'])
        messages.success(request, 'Alert dismissed.')
    return redirect('dashboard:patient_dashboard')


@role_required(User.Roles.CLINICIAN)
def clinician_dashboard(request):
    clinician = get_object_or_404(ClinicianProfile.objects.select_related('user'), user=request.user)
    patients = list(
        clinician.patients.select_related('user')
        .annotate(session_count=Count('sessions'))
        .order_by('external_id')
    )
    active = patients[0] if patients else None
    pid = request.GET.get('patient')
    if pid:
        active = next((p for p in patients if str(p.id) == str(pid)), active)

    frames = (
        list(
            PressureFrame.objects.filter(session__patient=active)
            .select_related('session')
            .order_by('-recorded_at')[:30]
        )
        if active
        else []
    )
    alerts = (
        PatientAlert.objects.filter(patient=active)
        .select_related('frame')
        .order_by('-created_at')[:10]
        if active
        else []
    )
    comments = (
        FrameComment.objects.filter(frame__session__patient=active, parent__isnull=True)
        .select_related('author', 'frame')
        .prefetch_related('replies__author')
        .order_by('-created_at')[:10]
        if active
        else []
    )
    reports = [
        {
            'frame': f,
            'risk': 'high' if f.peak_pressure_index >= 130 else 'medium' if f.peak_pressure_index >= 110 else 'low',
        }
        for f in frames[:8]
    ]
    return render(
        request,
        'dashboard/clinician_dashboard.html',
        {
            'clinician': clinician,
            'patients': patients,
            'active_patient': active,
            'alerts': alerts,
            'comments': comments,
            'reports': reports,
        },
    )


@role_required(User.Roles.CLINICIAN)
def review_alert(request, alert_id):
    clinician = get_object_or_404(ClinicianProfile, user=request.user)
    alert = get_object_or_404(PatientAlert, id=alert_id, patient__clinician=clinician)
    if request.method == 'POST':
        alert.reviewed = True
        alert.save(update_fields=['reviewed'])
        messages.success(request, 'Alert marked as reviewed.')
    return redirect(f"{redirect('dashboard:clinician_dashboard').url}?patient={alert.patient_id}")


@role_required(User.Roles.CLINICIAN)
def reply_comment(request, comment_id):
    clinician = get_object_or_404(ClinicianProfile, user=request.user)
    parent = get_object_or_404(
        FrameComment.objects.select_related('frame__session__patient'),
        id=comment_id,
        frame__session__patient__clinician=clinician,
    )
    if request.method == 'POST':
        message = (request.POST.get('message') or '').strip()
        if message:
            FrameComment.objects.create(
                frame=parent.frame,
                author=request.user,
                parent=parent,
                message=message,
            )
            messages.success(request, 'Reply added to comment.')
        else:
            messages.error(request, 'Reply message cannot be empty.')
    return redirect(f"{redirect('dashboard:clinician_dashboard').url}?patient={parent.frame.session.patient_id}")




@role_required(User.Roles.PATIENT)
def download_patient_report(request):
    patient = get_object_or_404(PatientProfile.objects.select_related('user'), user=request.user)
    sessions, selected_session, frames_qs = _filter_frames(
        patient, request.GET.get('day'), request.GET.get('interval', '24h')
    )
    frames = list(frames_qs)
    response = HttpResponse(content_type='text/csv')
    day_label = selected_session.session_date.isoformat() if selected_session else 'report'
    response['Content-Disposition'] = f'attachment; filename="graphene_trace_report_{patient.external_id}_{day_label}.csv"'
    response.write('patient_name,patient_id,session_date,interval,recorded_at,frame_index,peak_pressure_index,contact_area_percent,average_pressure,repositions_per_hour,flagged_for_review\n')

    for frame in frames:
        response.write(
            f'"{patient.user.get_full_name() or patient.user.username}",{patient.external_id},{selected_session.session_date if selected_session else ""},{request.GET.get("interval", "24h")},{frame.recorded_at.isoformat()},{frame.frame_index},{round(frame.peak_pressure_index,2)},{round(frame.contact_area_percent,2)},{round(frame.average_pressure,2)},{round(frame.reposition_per_hour,2)},{"Yes" if frame.flagged_for_review else "No"}'
        )
    return response

@role_required(User.Roles.CLINICIAN)
def clinician_download_patient_report(request, patient_id):
    clinician = get_object_or_404(ClinicianProfile, user=request.user)
    patient = get_object_or_404(PatientProfile.objects.select_related('user'), id=patient_id, clinician=clinician)
    sessions, selected_session, frames_qs = _filter_frames(
        patient, request.GET.get('day'), request.GET.get('interval', '24h')
    )
    frames = list(frames_qs)
    response = HttpResponse(content_type='text/csv')
    day_label = selected_session.session_date.isoformat() if selected_session else 'report'
    response['Content-Disposition'] = f'attachment; filename="graphene_trace_report_{patient.external_id}_{day_label}.csv"'
    response.write('patient_name,patient_id,session_date,interval,recorded_at,frame_index,peak_pressure_index,contact_area_percent,average_pressure,repositions_per_hour,flagged_for_review\n')
    for frame in frames:
        response.write(
            f'"{patient.user.get_full_name() or patient.user.username}",{patient.external_id},{selected_session.session_date if selected_session else ""},{request.GET.get("interval", "24h")},{frame.recorded_at.isoformat()},{frame.frame_index},{round(frame.peak_pressure_index,2)},{round(frame.contact_area_percent,2)},{round(frame.average_pressure,2)},{round(frame.reposition_per_hour,2)},{"Yes" if frame.flagged_for_review else "No"}\n'
        )
    return response

from .forms import PatientClinicianRegistrationForm

def register(request):
    form = PatientClinicianRegistrationForm()
    if request.method == 'POST':
        form = PatientClinicianRegistrationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            external = form.cleaned_data['external_id'] or (
                'P-XXXX' if role == 'patient' else 'C-XXXX'
            )
            password = form.cleaned_data['password']

            # Generate unique username
            base = (first or email.split('@')[0]).lower()
            username = base
            i = 1
            while User.objects.filter(username=username).exists():
                i += 1
                username = f'{base}{i}'

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first,
                last_name=last,
                email=email,
                role=role,
            )
            if role == 'clinician':
                ClinicianProfile.objects.create(user=user, specialty='General')
            elif role == 'patient':
                PatientProfile.objects.create(
                    user=user,
                    external_id=external,
                    clinician=ClinicianProfile.objects.first(),
                )
            messages.success(request, f'Account created! You can now log in as {first}.')
            return redirect('login')
    return render(request, 'registration/register.html', {'form': form})


@role_required(User.Roles.ADMIN)
def admin_dashboard(request):
    form = AccountCreationForm()
    if request.method == 'POST' and request.POST.get('action') == 'create_account':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            external = form.cleaned_data['external_id'] or (
                'P-XXXX' if role == User.Roles.PATIENT else 'C-XXXX'
            )
            username = (first or email.split('@')[0]).lower()
            base = username
            i = 1
            while User.objects.filter(username=username).exists():
                i += 1
                username = f'{base}{i}'
            user = User.objects.create_user(
                username=username,
                password=f'{username}@123',
                first_name=first,
                last_name=last,
                email=email,
                role=role,
            )
            if role == User.Roles.CLINICIAN:
                ClinicianProfile.objects.create(user=user, specialty='Wound Care')
            elif role == User.Roles.PATIENT:
                PatientProfile.objects.create(
                    user=user,
                    external_id=external,
                    clinician=ClinicianProfile.objects.first(),
                )
            messages.success(request, f'Created {role} account for {first}.')
            return redirect('dashboard:admin_dashboard')

    if request.method == 'POST' and request.POST.get('action') == 'toggle_access':
        user = get_object_or_404(User, id=request.POST.get('user_id'))
        if user != request.user:
            user.is_active = not user.is_active
            user.save(update_fields=['is_active'])
            messages.success(request, f'Updated access for {user.username}.')
        return redirect('dashboard:admin_dashboard')

    return render(
        request,
        'dashboard/admin_dashboard.html',
        {
            'create_form': form,
            'recent_accounts': list(User.objects.order_by('-date_joined')[:6]),
            'accounts': list(User.objects.exclude(role=User.Roles.ADMIN).order_by('role', 'username')),
            'patient_count': PatientProfile.objects.count(),
            'clinician_count': ClinicianProfile.objects.count(),
        },
    )
