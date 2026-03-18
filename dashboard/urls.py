from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('redirect/', views.role_redirect, name='role_redirect'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('clinician/', views.clinician_dashboard, name='clinician_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]
