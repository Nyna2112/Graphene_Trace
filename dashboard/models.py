from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class ClinicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clinician_profile')
    specialty = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    clinician = models.ForeignKey(ClinicianProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class BloodPressureReport(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='bp_reports')
    systolic = models.PositiveIntegerField()
    diastolic = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('high', 'High'), ('normal', 'Normal'), ('low', 'Low')])
    recorded_at = models.DateTimeField()

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f'{self.patient} - {self.systolic}/{self.diastolic} ({self.status})'

class SymptomUpdate(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='symptom_updates')
    symptoms = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Consultation(models.Model):
    clinician = models.ForeignKey(ClinicianProfile, on_delete=models.CASCADE, related_name='consultations')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='consultations')
    summary = models.CharField(max_length=255)
    consultation_date = models.DateField()
    reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-consultation_date', '-id']

class Prescription(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prescriptions')
    clinician = models.ForeignKey(ClinicianProfile, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.CharField(max_length=120)
    dosage = models.CharField(max_length=120)
    issued_at = models.DateField()

    class Meta:
        ordering = ['-issued_at', '-id']

class WeeklyLog(models.Model):
    clinician = models.ForeignKey(ClinicianProfile, on_delete=models.CASCADE, related_name='weekly_logs')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='weekly_logs')
    week_start = models.DateField()
    note = models.CharField(max_length=255)

    class Meta:
        ordering = ['-week_start', '-id']

class Feedback(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveSmallIntegerField(default=5)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=120)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class SystemAlert(models.Model):
    level = models.CharField(max_length=20, choices=[('info', 'Info'), ('warning', 'Warning'), ('critical', 'Critical')])
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
