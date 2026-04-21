import csv, zipfile
from datetime import datetime, timedelta
from pathlib import Path
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from dashboard.models import ClinicianProfile, PatientAlert, PatientProfile, PressureFrame, PressureSession
from dashboard.utils import HIGH_PRESSURE_THRESHOLD, compute_frame_metrics
User=get_user_model()
PATIENTS=[('kartheek','Kartheek','1c0fd777','P-001'),('neyana','Neyana','543d4676','P-002'),('priyanka','Priyanka','71e66ab3','P-003'),('mahesh','Mahesh','d13043b3','P-004'),('shankar','Shankar','de0e9b2c','P-005')]
class Command(BaseCommand):
  help='Seed demo users and import GTLB sample data.'
  def add_arguments(self, parser): parser.add_argument('--zip-path',default='sample_data/GTLB-Data.zip'); parser.add_argument('--samples-per-day',type=int,default=48)
  @transaction.atomic
  def handle(self,*args,**opts):
    zp=Path(opts['zip_path']); zp=zp if zp.is_absolute() else Path.cwd()/zp; samples=opts['samples_per_day']
    PressureFrame.objects.all().delete(); PressureSession.objects.all().delete(); PatientAlert.objects.all().delete(); PatientProfile.objects.all().delete(); ClinicianProfile.objects.all().delete(); User.objects.all().delete()
    User.objects.create_user('admin',password='admin@123',first_name='Admin',role=User.Roles.ADMIN,is_staff=True,is_superuser=True)
    cu=User.objects.create_user('clinician',password='clinician@123',first_name='Clinician',role=User.Roles.CLINICIAN); clinician=ClinicianProfile.objects.create(user=cu,specialty='Pressure Injury Monitoring')
    patients={}
    for username,first,sensor,ext in PATIENTS:
      u=User.objects.create_user(username,password=f'{username}@123',first_name=first,email=f'{username}@example.com',role=User.Roles.PATIENT)
      patients[sensor]=PatientProfile.objects.create(user=u,external_id=ext,clinician=clinician,sensor_code=sensor)
    with zipfile.ZipFile(zp) as zf:
      for fname in sorted([n for n in zf.namelist() if n.endswith('.csv') and '/._' not in n and '__MACOSX' not in n]):
        sensor=Path(fname).name.split('_')[0]; patient=patients.get(sensor)
        if not patient: continue
        day=datetime.strptime(Path(fname).stem.split('_')[1],'%Y%m%d').date(); start=timezone.make_aware(datetime.combine(day, datetime.min.time())); session=PressureSession.objects.create(patient=patient,source_file=Path(fname).name,session_date=day,started_at=start)
        with zf.open(fname) as fh: rows=[list(map(float,row)) for row in csv.reader(line.decode('utf-8') for line in fh) if row and len(row)==32]
        frame_count=len(rows)//32
        if frame_count==0: continue
        step=max(1, frame_count//samples); chosen=list(range(0,frame_count,step))[:samples]
        prev=False
        for out_i, frame_i in enumerate(chosen):
          matrix=rows[frame_i*32:(frame_i+1)*32]; seconds=int((frame_i/max(1,frame_count-1))*(24*60*60-1)); recorded=start+timedelta(seconds=seconds); metrics=compute_frame_metrics(matrix)
          frame=PressureFrame.objects.create(session=session,frame_index=out_i,recorded_at=recorded,matrix_json=matrix,**metrics)
          if metrics['flagged_for_review'] and not prev: PatientAlert.objects.create(patient=patient,frame=frame,level=PatientAlert.Levels.CRITICAL if metrics['peak_pressure_index']>=HIGH_PRESSURE_THRESHOLD+20 else PatientAlert.Levels.WARNING,message=f'High pressure detected around {recorded.strftime("%H:%M")}.')
          prev=metrics['flagged_for_review']
        session.frame_count=len(chosen); session.save(update_fields=['frame_count'])
    self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
