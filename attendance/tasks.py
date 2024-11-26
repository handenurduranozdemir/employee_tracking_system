from celery import shared_task
from .models import Attendance, MonthlyReport
from django.utils.timezone import now
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from leave.models import EmployeeProfile
from datetime import timedelta, datetime

@shared_task
def notify_late_employees():
    try:
        late_employees = Attendance.objects.filter(
            date=now().date(),
            check_in__gt='08:00'
        )
        if late_employees.exists():
            message = {
                'title': 'Geç Kalma Bildirimi',
                'body': f'{late_employees.count()} çalışan bugün geç kaldı.'
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'attendance_notifications', {
                    'type': 'send_notification',
                    'message': message
                }
            )
    except Exception as e:
        print(f"Celery task error: {e}")

@shared_task
def test_celery():
    print("Celery test task executed!")

@shared_task
def calculate_late_deductions():
    today = now().date()
    attendances = Attendance.objects.filter(date=today)

    for attendance in attendances:
        late_minutes = attendance.late_minutes()
        if late_minutes > 0:  # Eğer geç kalmışsa
            profile = EmployeeProfile.objects.get(user=attendance.employee)
            profile.deduct_lateness(late_minutes)


@shared_task
def generate_monthly_reports():
    today = now().date()
    first_day_of_month = today.replace(day=1)
    last_month = first_day_of_month - timedelta(days=1)

    employees = Attendance.objects.values_list('employee', flat=True).distinct()
    for employee_id in employees:
        attendances = Attendance.objects.filter(
            employee_id=employee_id,
            date__month=last_month.month,
            date__year=last_month.year
        )
        total_working_hours = sum((attendance.working_hours() for attendance in attendances), timedelta())

        MonthlyReport.objects.update_or_create(
            employee_id=employee_id,
            month=last_month.replace(day=1),
            defaults={'total_working_hours': total_working_hours}
        )