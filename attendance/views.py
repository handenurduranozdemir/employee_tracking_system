from django.shortcuts import render
from .models import Attendance, MonthlyReport
from django.contrib.auth.decorators import login_required



def manager_dashboard(request):
    attendances = Attendance.objects.all().order_by('-date')

    context = {
        'attendances': attendances,
    }

    return render(request, 'attendance/manager_dashboard.html', context)


@login_required
def monthly_report_view(request):
    reports = MonthlyReport.objects.filter(employee=request.user).order_by('-month')
    context = {
        'reports': reports
    }
    return render(request, 'attendance/monthly_report.html', context)