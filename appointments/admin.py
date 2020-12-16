from django.contrib import admin

from .models import Appointment, Doctor


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'doctor', 'patient')
    list_filter = ('date', 'doctor')
    search_fields = ('date', 'doctor')


class DoctorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
