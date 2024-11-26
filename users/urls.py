from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee-list/', views.employee_list, name='employee_list'),
    path('employee-detail/<int:user_id>/', views.employee_detail, name='employee_detail'),
]
