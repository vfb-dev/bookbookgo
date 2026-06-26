import uuid
from datetime import time

from django.db import models
from django.db.models import Q


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AvailabilityRule(models.Model):
    WEEKDAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField(default=time(9, 0))
    end_time = models.TimeField(default=time(17, 0))
    slot_duration_minutes = models.PositiveIntegerField(default=60)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["weekday", "start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["weekday", "start_time", "end_time"],
                name="unique_availability_rule",
            )
        ]

    def __str__(self):
        return (
            f"{self.get_weekday_display()} "
            f"{self.start_time.strftime('%I:%M %p')} - "
            f"{self.end_time.strftime('%I:%M %p')}"
        )


class BlockedDate(models.Model):
    date = models.DateField(unique=True)
    reason = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        if self.reason:
            return f"{self.date} - {self.reason}"

        return str(self.date)


class Appointment(models.Model):

    class Meta:
        ordering = ["appointment_date", "appointment_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["appointment_date", "appointment_time"],
                condition=~Q(status="cancelled"),
                name="unique_appointment_slot",
            )
        ]

    SERVICE_CHOICES = [
        ("tax", "Tax consultation"),
        ("bookkeeping", "Bookkeeping setup"),
        ("payroll", "Payroll review"),
        ("business_finance", "Business finance consultation"),
        ("personal_finance", "Personal finance consultation"),
    ]

    BUSINESS_TYPE_CHOICES = [
        ("individual", "Individual"),
        ("freelancer", "Freelancer"),
        ("small_business", "Small business"),
        ("llc_corp", "LLC / Corporation"),
        ("nonprofit", "Nonprofit"),
        ("other", "Other"),
    ]

    TIME_CHOICES = [
        (time(9, 0), "9:00 AM"),
        (time(10, 0), "10:00 AM"),
        (time(11, 0), "11:00 AM"),
        (time(13, 0), "1:00 PM"),
        (time(14, 0), "2:00 PM"),
        (time(15, 0), "3:00 PM"),
        (time(16, 0), "4:00 PM"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    business_name = models.CharField(max_length=120, blank=True)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    public_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def get_status_badge_class(self):
        badge_classes = {
            "pending": "bg-warning text-dark",
            "confirmed": "bg-success",
            "cancelled": "bg-danger",
            "completed": "bg-secondary",
        }

        return badge_classes.get(self.status, "bg-secondary")
