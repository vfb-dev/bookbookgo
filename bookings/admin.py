from django.contrib import admin
from .models import Appointment, Service

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_minutes", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "service",
        "appointment_date",
        "appointment_time",
        "status",
        "email",
        "phone",
        "created_at",
    )
    list_filter = ("status", "service", "appointment_date", "business_type")
    search_fields = ("full_name", "email", "phone", "business_name")
    list_editable = ("status",)