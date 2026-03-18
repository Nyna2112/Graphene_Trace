import json
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import role_required
from .forms import SymptomUpdateForm
from .models import (
    ActivityLog,
    BloodPressureReport,
    ClinicianProfile,
    Consultation,
    Feedback,
    PatientProfile,
    Prescription,
    SystemAlert,
    WeeklyLog,
)

User = get_user_model()

@login_required
def role_redirect(request):
    if request.user.role == User.Roles.ADMIN:
        return redirect('dashboard:admin_dashboard')
    if request.user.role == User.Roles.CLINICIAN:
        return redirect('dashboard:clinician_dashboard')
    return redirect('dashboard:patient_dashboard')

@role_required(User.Roles.PATIENT)
def patient_dashboard(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    latest_report = patient.bp_reports.first()
    recent_reports = list(patient.bp_reports.order_by('recorded_at')[:7])
    form = SymptomUpdateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        update = form.save(commit=False)
        update.patient = patient
        update.save()
        ActivityLog.objects.create(user=request.user, action='Symptom Update', details='Patient submitted symptoms.')
        messages.success(request, 'Symptoms updated successfully.')
        return redirect('dashboard:patient_dashboard')

    chart_labels = [report.recorded_at.strftime('%b %d') for report in recent_reports]
    systolic_data = [report.systolic for report in recent_reports]
    diastolic_data = [report.diastolic for report in recent_reports]

    context = {
        'patient': patient,
        'latest_report': latest_report,
        'form': form,
        'chart_labels': json.dumps(chart_labels),
        'systolic_data': json.dumps(systolic_data),
        'diastolic_data': json.dumps(diastolic_data),
    }
    return render(request, 'dashboard/patient_dashboard.html', context)

@role_required(User.Roles.CLINICIAN)
def clinician_dashboard(request):
    clinician = get_object_or_404(ClinicianProfile, user=request.user)
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())

    todays_patient_count = Consultation.objects.filter(clinician=clinician, consultation_date=today).values('patient').distinct().count()
    recent_consultations_count = Consultation.objects.filter(clinician=clinician, consultation_date__gte=today - timedelta(days=7)).count()
    pending_reviews_count = Consultation.objects.filter(clinician=clinician, reviewed=False).count()
    high_bp_alerts = BloodPressureReport.objects.filter(patient__clinician=clinician, status='high').select_related('patient__user')[:5]
    weekly_logs = WeeklyLog.objects.filter(clinician=clinician, week_start__gte=week_start).select_related('patient__user')[:10]
    prescription_history = Prescription.objects.filter(clinician=clinician).select_related('patient__user')[:8]

    context = {
        'clinician': clinician,
        'todays_patient_count': todays_patient_count,
        'recent_consultations_count': recent_consultations_count,
        'pending_reviews_count': pending_reviews_count,
        'high_bp_alerts': high_bp_alerts,
        'weekly_logs': weekly_logs,
        'prescription_history': prescription_history,
    }
    return render(request, 'dashboard/clinician_dashboard.html', context)

@role_required(User.Roles.ADMIN)
def admin_dashboard(request):
    clinician_count = ClinicianProfile.objects.count()
    recent_activity = ActivityLog.objects.select_related('user')[:8]
    system_alerts = SystemAlert.objects.all()[:5]
    clinicians = ClinicianProfile.objects.select_related('user').all()
    patients = PatientProfile.objects.select_related('user', 'clinician__user').all()[:10]
    users = User.objects.all()[:10]
    feedbacks = Feedback.objects.select_related('patient__user').all()[:8]
    avg_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg'] or 0

    context = {
        'clinician_count': clinician_count,
        'recent_activity': recent_activity,
        'system_alerts': system_alerts,
        'clinicians': clinicians,
        'patients': patients,
        'users': users,
        'feedbacks': feedbacks,
        'avg_rating': round(avg_rating, 2),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
