from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm
from users.models import CustomUser
from leave.models import EmployeeProfile
from attendance.models import Attendance
from django.db.models import Sum, F, ExpressionWrapper, DurationField


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Role göre yönlendirme
            if user.is_superuser:
                return redirect('manager_dashboard')
            elif user.role == 'manager':
                return redirect('manager_dashboard')
            else:
                return redirect('employee_dashboard')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def employee_dashboard(request):
    return render(request, 'users/employee_dashboard.html')

@login_required
def manager_dashboard(request):
    return render(request, 'users/manager_dashboard.html')


@login_required
def employee_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/employee_list.html', {'users': users})


@login_required
def employee_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    profile = get_object_or_404(EmployeeProfile, user=user)
    attendances = Attendance.objects.filter(employee=user)
    
    # Geç kalma sürelerinin toplamını hesapla
    total_late_minutes = sum(attendance.calculate_lateness() for attendance in attendances)

    # Aylık toplam çalışma saatlerini hesapla
    monthly_working_hours = attendances.aggregate(
        total_hours=Sum(ExpressionWrapper(F('check_out') - F('check_in'), output_field=DurationField()))
    )['total_hours']

    context = {
        'user': user,
        'profile': profile,
        'attendances': attendances,
        'total_late_minutes': total_late_minutes,
        'monthly_working_hours': monthly_working_hours,
    }
    return render(request, 'users/employee_detail.html', context)