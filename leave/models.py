from django.db import models
from django.conf import settings
from math import ceil

class Leave(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def leave_days(self):
        """Toplam izin günlerini hesaplar."""
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.employee.username} - {self.start_date} to {self.end_date}"

class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    remaining_leaves = models.IntegerField(default=15)  # Yeni çalışanlara varsayılan olarak 15 gün izin
    total_late_minutes = models.PositiveIntegerField(default=0)  # Toplam geç kalma süresi

    def deduct_lateness(self, total_late_minutes):
        """Geç kalma süresini kalan izinlerden düş."""
        late_days = ceil(total_late_minutes / (8 * 60))  # Her 8 saat bir gün sayılır
        self.deduct_leaves(late_days)

    def deduct_leaves(self, days):
        """Kalan izinlerden düşülür."""
        if self.remaining_leaves >= days:
            self.remaining_leaves -= days
        else:
            self.remaining_leaves = 0
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def deduct_leaves_for_lateness(self):
        """Toplam geç kalma süresini gün olarak hesaplayıp yıllık izinden düşer."""
        late_days = self.total_late_minutes // 480  # 1 gün = 8 saat = 480 dakika
        self.remaining_leaves = max(self.remaining_leaves - late_days, 0)
        self.total_late_minutes %= 480  # Artan geç kalma dakikaları sonraki aya aktarılır
        self.save()

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.start_date} to {self.end_date} ({self.get_status_display()})"

