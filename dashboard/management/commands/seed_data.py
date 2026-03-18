from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from dashboard.models import (
    ActivityLog, BloodPressureReport, ClinicianProfile, Consultation,
    Feedback, PatientProfile, Prescription, SystemAlert, WeeklyLog,
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with demo HealthCare data.'

    def handle(self, *args, **options):
        admin_user, _ = User.objects.get_or_create(username='admin', defaults={
            'role': User.Roles.ADMIN,
            'is_staff': True,
            'is_superuser': True,
            'email': 'admin@example.com',
            'first_name': 'System',
            'last_name': 'Admin',
        })
        admin_user.role = User.Roles.ADMIN
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password('admin123')
        admin_user.save()

        clinician_user, _ = User.objects.get_or_create(username='clinician1', defaults={
            'role': User.Roles.CLINICIAN,
            'email': 'clinician1@example.com',
            'first_name': 'Ava',
            'last_name': 'Stone',
        })
        clinician_user.role = User.Roles.CLINICIAN
        clinician_user.set_password('clinician123')
        clinician_user.save()
        clinician, _ = ClinicianProfile.objects.get_or_create(user=clinician_user, defaults={
            'specialty': 'Cardiology',
            'phone': '+1-555-2200',
            'status': 'active',
        })

        patient_user, _ = User.objects.get_or_create(username='patient1', defaults={
            'role': User.Roles.PATIENT,
            'email': 'patient1@example.com',
            'first_name': 'Liam',
            'last_name': 'Turner',
        })
        patient_user.role = User.Roles.PATIENT
        patient_user.set_password('patient123')
        patient_user.save()
        patient, _ = PatientProfile.objects.get_or_create(user=patient_user, defaults={
            'clinician': clinician,
            'age': 42,
            'gender': 'Male',
        })
        patient.clinician = clinician
        patient.save()

        patient2_user, _ = User.objects.get_or_create(username='patient2', defaults={
            'role': User.Roles.PATIENT,
            'email': 'patient2@example.com',
            'first_name': 'Emma',
            'last_name': 'Hart',
        })
        patient2_user.role = User.Roles.PATIENT
        patient2_user.set_password('patient123')
        patient2_user.save()
        patient2, _ = PatientProfile.objects.get_or_create(user=patient2_user, defaults={
            'clinician': clinician,
            'age': 55,
            'gender': 'Female',
        })
        patient2.clinician = clinician
        patient2.save()

        now = timezone.now()
        report_samples = [
            (patient, 150, 95, 'high', 6),
            (patient, 145, 92, 'high', 5),
            (patient, 138, 88, 'normal', 4),
            (patient, 132, 84, 'normal', 3),
            (patient, 129, 82, 'normal', 2),
            (patient, 124, 80, 'normal', 1),
            (patient, 142, 90, 'high', 0),
            (patient2, 155, 98, 'high', 0),
        ]
        for p, sys, dia, status, days_ago in report_samples:
            BloodPressureReport.objects.get_or_create(
                patient=p,
                systolic=sys,
                diastolic=dia,
                status=status,
                recorded_at=now - timedelta(days=days_ago),
            )

        for idx in range(1, 6):
            Consultation.objects.get_or_create(
                clinician=clinician,
                patient=patient if idx % 2 else patient2,
                summary=f'Consultation summary {idx}',
                consultation_date=timezone.localdate() - timedelta(days=idx-1),
                reviewed=(idx % 2 == 0),
            )

        for idx in range(1, 5):
            Prescription.objects.get_or_create(
                patient=patient if idx % 2 else patient2,
                clinician=clinician,
                medication=f'Medication {idx}',
                dosage=f'{idx} tablet(s) daily',
                issued_at=timezone.localdate() - timedelta(days=idx * 3),
            )

        for idx in range(3):
            WeeklyLog.objects.get_or_create(
                clinician=clinician,
                patient=patient if idx % 2 == 0 else patient2,
                week_start=timezone.localdate() - timedelta(days=timezone.localdate().weekday()),
                note=f'Weekly follow-up note {idx + 1}',
            )

        Feedback.objects.get_or_create(patient=patient, rating=5, message='Very supportive care and quick follow-up.')
        Feedback.objects.get_or_create(patient=patient2, rating=4, message='Good consultation and clear prescription guidance.')

        ActivityLog.objects.get_or_create(user=admin_user, action='System Check', details='Admin reviewed system status.')
        ActivityLog.objects.get_or_create(user=clinician_user, action='Consultation Review', details='Clinician reviewed pending cases.')
        ActivityLog.objects.get_or_create(user=patient_user, action='Report View', details='Patient viewed the latest BP report.')

        SystemAlert.objects.get_or_create(level='warning', message='2 patients have elevated blood pressure trends.')
        SystemAlert.objects.get_or_create(level='info', message='Nightly backup completed successfully.')
        SystemAlert.objects.get_or_create(level='critical', message='Pending review queue requires clinician attention.')

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
