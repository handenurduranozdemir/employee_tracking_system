from django.urls import path
from . import views
from .views import test_email_view

urlpatterns = [
    path('leave-summary/', views.leave_summary, name='leave_summary'),
    path('define-leave/', views.define_leave, name='define_leave'),
    path('request-leave/', views.request_leave, name='request_leave'),
    path('manage-leave-requests/', views.manage_leave_requests, name='manage_leave_requests'),
    path('update-leave-request/<int:request_id>/<str:action>/', views.update_leave_request, name='update_leave_request'),
    path('test-email/', test_email_view, name='test_email'),
]
