from django.contrib import admin
from .models import (
    ActivityLog, BloodPressureReport, ClinicianProfile, Consultation,
    Feedback, PatientProfile, Prescription, SymptomUpdate, SystemAlert, WeeklyLog
)

admin.site.register(ClinicianProfile)
admin.site.register(PatientProfile)
admin.site.register(BloodPressureReport)
admin.site.register(SymptomUpdate)
admin.site.register(Consultation)
admin.site.register(Prescription)
admin.site.register(WeeklyLog)
admin.site.register(Feedback)
admin.site.register(ActivityLog)
admin.site.register(SystemAlert)
