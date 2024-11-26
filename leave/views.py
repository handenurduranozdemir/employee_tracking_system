from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LeaveForm, LeaveRequestForm

from .models import LeaveRequest
from .models import Leave, EmployeeProfile

@login_required
def leave_summary(request):
    employee = request.user
    profile, created = EmployeeProfile.objects.get_or_create(user=employee)
    leaves = Leave.objects.filter(employee=employee)

    context = {
        'profile': profile,
        'leaves': leaves,
        'remaining_leaves': employee.profile.remaining_leaves,
    }
    return render(request, 'leave/leave_summary.html', context)


# Sadece yetkililerin erişimine izin veren kontrol
def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

@login_required
@user_passes_test(is_manager)
def define_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')  # Yetkili dashboard'una yönlendirme
    else:
        form = LeaveForm()
    
    context = {'form': form}
    return render(request, 'leave/define_leave.html', context)


@login_required
def request_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            return redirect('employee_dashboard')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave/request_leave.html', {'form': form})

@login_required
def manage_leave_requests(request):
    if request.user.role != 'manager':
        return redirect('employee_dashboard')
    
    leave_requests = LeaveRequest.objects.filter(status='pending').order_by('-created_at')
    
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')

        leave_request = get_object_or_404(LeaveRequest, id=leave_id)

        if action == 'approve':
            leave_request.status = 'approved'
        elif action == 'reject':
            leave_request.status = 'rejected'

        leave_request.save()

        return redirect('manage_leave_requests')

    return render(request, 'leave/manage_leave_requests.html', {'leave_requests': leave_requests})

@login_required
def update_leave_request(request, request_id, action):
    leave_request = get_object_or_404(LeaveRequest, id=request_id)
    if request.user.is_manager:
        if action == 'approve':
            leave_request.status = 'approved'
        elif action == 'reject':
            leave_request.status = 'rejected'
        leave_request.save()
    return redirect('manage_leave_requests')

from django.core.mail import send_mail
from django.http import HttpResponse

def test_email_view(request):
    send_mail(
        subject='Test E-mail',
        message='This is a test email sent from console backend.',
        from_email='system@example.com',
        recipient_list=['to@example.com'],
        fail_silently=False,
    )
    return HttpResponse("E-posta gönderildi ve terminale yazdırıldı!")

