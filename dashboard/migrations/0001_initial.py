from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('info', 'Info'), ('warning', 'Warning'), ('critical', 'Critical')], max_length=20)),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ClinicianProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty', models.CharField(blank=True, max_length=120)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clinician_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(default=0)),
                ('gender', models.CharField(blank=True, max_length=20)),
                ('clinician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='dashboard.clinicianprofile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(default=5)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='dashboard.patientprofile')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='BloodPressureReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('systolic', models.PositiveIntegerField()),
                ('diastolic', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('high', 'High'), ('normal', 'Normal'), ('low', 'Low')], max_length=20)),
                ('recorded_at', models.DateTimeField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bp_reports', to='dashboard.patientprofile')),
            ],
            options={'ordering': ['-recorded_at']},
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=255)),
                ('consultation_date', models.DateField()),
                ('reviewed', models.BooleanField(default=False)),
                ('clinician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='dashboard.clinicianprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='dashboard.patientprofile')),
            ],
            options={'ordering': ['-consultation_date', '-id']},
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication', models.CharField(max_length=120)),
                ('dosage', models.CharField(max_length=120)),
                ('issued_at', models.DateField()),
                ('clinician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='dashboard.clinicianprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='dashboard.patientprofile')),
            ],
            options={'ordering': ['-issued_at', '-id']},
        ),
        migrations.CreateModel(
            name='SymptomUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptoms', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symptom_updates', to='dashboard.patientprofile')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='WeeklyLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_start', models.DateField()),
                ('note', models.CharField(max_length=255)),
                ('clinician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_logs', to='dashboard.clinicianprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_logs', to='dashboard.patientprofile')),
            ],
            options={'ordering': ['-week_start', '-id']},
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=120)),
                ('details', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
