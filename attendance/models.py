from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import date, timedelta, datetime
from django.utils.timezone import now

class Attendance(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)  # Giriş tarihi
    check_in = models.TimeField(null=True, blank=True)  # İlk giriş saati
    check_out = models.TimeField(null=True, blank=True)  # Son çıkış saati
    late_minutes = models.PositiveIntegerField(default=0) # Geç kalma süresini dakika olarak tutar

    def late_by(self):
        """Geç kalma süresini hesaplar."""
        company_start_time = datetime.strptime("08:00", "%H:%M").time()
        if self.check_in and self.check_in > company_start_time:
            late_duration = datetime.combine(self.date, self.check_in) - datetime.combine(self.date, company_start_time)
            return late_duration
        return timedelta(0)

    def __str__(self):
        return f"{self.employee.username} - {self.date}"
    
    def is_weekend(self):
        """Tatil günü (Cumartesi veya Pazar) kontrolü."""
        return self.date.weekday() in [5, 6] 
    
    def clean(self):
        if self.date.weekday() in [5, 6]:
            raise ValidationError('Tatil günlerinde giriş yapılamaz.')
        super().clean()

    '''def late_minutes(self):
        """Geç kalma süresini dakika bazında hesaplar."""
        work_start_time = datetime.strptime('08:00', '%H:%M').time()
        if self.check_in > work_start_time:
            delta = datetime.combine(self.date, self.check_in) - datetime.combine(self.date, work_start_time)
            return delta.total_seconds() / 60  # Dakika cinsinden döndür
        return 0  # Geç kalma yoksa 0 dakika'''
    
    def calculate_lateness(self):
        """Geç kalma süresini dakika bazında hesaplar."""
        if self.check_in is None:
            return 0  # Giriş saati yoksa geç kalma yok

        work_start_time = datetime.strptime('08:00', '%H:%M').time()
        
        if self.check_in > work_start_time:
            delta = datetime.combine(self.date, self.check_in) - datetime.combine(self.date, work_start_time)
            return int(delta.total_seconds() / 60)  # Dakika cinsinden döndür
        return 0  # Geç kalma yoksa 0 dakika
  
    def working_hours(self):
        """Çalışma saatlerini hesaplar."""
        if not self.check_in or not self.check_out:
            return timedelta(0)  # Giriş veya çıkış eksikse, sıfır süre döndür
        try:
            delta = datetime.combine(date.min, self.check_out) - datetime.combine(date.min, self.check_in)
            return max(delta, timedelta(0))  # Negatif süreleri 0'a indirger
        except Exception as e:
            print(f"Çalışma saatlerini hesaplama hatası: {e}")
            return timedelta(0)


class MonthlyReport(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='monthly_reports')
    month = models.DateField()  # Ayın ilk günü
    total_working_hours = models.DurationField(default=timedelta)

    def __str__(self):
        return f"{self.employee.username} - {self.month.strftime('%B %Y')}"

    

    
