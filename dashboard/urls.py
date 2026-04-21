from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.role_redirect, name='role_redirect'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/dismiss-alert/<int:alert_id>/', views.dismiss_patient_alert, name='dismiss_patient_alert'),
    path('patient/download-report/', views.download_patient_report, name='download_patient_report'),
    path('clinician/', views.clinician_dashboard, name='clinician_dashboard'),
    path('clinician/review-alert/<int:alert_id>/', views.review_alert, name='review_alert'),
    path('clinician/reply-comment/<int:comment_id>/', views.reply_comment, name='reply_comment'),
    path('clinician/download-report/<int:patient_id>/', views.clinician_download_patient_report, name='clinician_download_patient_report'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register, name='register'),
    
]
