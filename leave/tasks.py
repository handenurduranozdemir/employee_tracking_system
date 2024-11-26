from celery import shared_task
from .models import EmployeeProfile
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def process_monthly_lateness():
    profiles = EmployeeProfile.objects.all()
    for profile in profiles:
        profile.deduct_leaves_for_lateness()

@shared_task
def notify_manager_about_leaves(username, remaining_leaves, manager_emails):
    send_mail(
        subject="Yıllık İzin Uyarısı",
        message=f"{username} adlı çalışanınızın yıllık izni 3 günden azdır. Mevcut izin: {remaining_leaves} gün.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=manager_emails,
        fail_silently=False,
    )

@shared_task
def update_lateness_for_all_employees():
    """Tüm çalışanların geç kalma sürelerini kontrol eder ve yıllık izinden düşer."""
    profiles = EmployeeProfile.objects.all()
    for profile in profiles:
        profile.deduct_leaves_for_lateness()