from django.urls import path
from . import views

urlpatterns = [
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('monthly-report/', views.monthly_report_view, name='monthly_report'),
]
