from django.contrib import admin
from .models import Attendance
from django.utils.timezone import now
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django import forms

class AttendanceAdminForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'check_in': TimePickerInput(format='%H:%M'),
            'check_out': TimePickerInput(format='%H:%M'),
        }

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceAdminForm
    list_display = ('employee', 'date', 'check_in', 'check_out', 'late_by')
    list_filter = ('date',)
    search_fields = ('employee__username',)
    fields = ('employee', 'date', 'check_in', 'check_out')  # Hangi alanların admin panelinde görüneceğini düzenleyin.

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['date'].initial = now().date()  # Varsayılan olarak bugünü seç
        return form
