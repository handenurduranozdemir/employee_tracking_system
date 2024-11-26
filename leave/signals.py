from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from .tasks import notify_manager_about_leaves

from .models import EmployeeProfile
from attendance.models import Attendance

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(user=instance)

@receiver(post_save, sender=EmployeeProfile)
def check_remaining_leaves(sender, instance, **kwargs):
    if instance.remaining_leaves < 3:
        # Yetkili kişilerin e-posta adreslerini al
        manager_emails = [user.email for user in sender.objects.filter(user__role='manager')]
        
        if instance.remaining_leaves < 3:
            manager_emails = [user.email for user in sender.objects.filter(user__role='manager')]
            notify_manager_about_leaves.delay(instance.user.username, instance.remaining_leaves, manager_emails)

        # Bildirim e-postası gönder
        send_mail(
            subject="Yıllık İzin Uyarısı",
            message=f"{instance.user.username} adlı çalışanınızın yıllık izni 3 günden azdır. Mevcut izin: {instance.remaining_leaves} gün.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=manager_emails,
            fail_silently=False,
        )

@receiver(post_save, sender=Attendance)
def update_total_late_minutes(sender, instance, **kwargs):
    """Geç kalma süresini EmployeeProfile modeline ekler."""
    if instance.check_in:
        late_minutes = instance.calculate_lateness()  # Geç kalma süresini hesapla
        
        # Çalışanın profilini al ve total_late_minutes değerini güncelle
        try:
            profile = EmployeeProfile.objects.get(user=instance.employee)
            profile.total_late_minutes += late_minutes
            profile.save()
        except EmployeeProfile.DoesNotExist:
            pass  # Eğer profil yoksa bir şey yapma


@receiver(post_save, sender=Attendance)
def update_lateness_and_leaves(sender, instance, **kwargs):
    """Geç kalma süresini hesaplayıp yıllık izinden düşer."""
    if instance.check_in:  # Eğer giriş saati varsa
        try:
            profile = EmployeeProfile.objects.get(user=instance.employee)
            late_minutes = instance.calculate_lateness()  # Geç kalma süresini hesapla
            
            # Toplam geç kalma süresini güncelle
            profile.total_late_minutes += late_minutes
            profile.deduct_leaves_for_lateness()  # Geç kalma süresini yıllık izinden düş
        except EmployeeProfile.DoesNotExist:
            pass  # Profil bulunamazsa bir şey yapmayın