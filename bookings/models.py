from django.db import models
from datetime import time

# Create your models here.
class Appointment(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["appointment_date", "appointment_time"],
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

    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(choices=TIME_CHOICES)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    business_name = models.CharField(max_length=120, blank=True)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_status_badge_class(self):
        badge_classes = {
            "pending": "bg-warning text-dark",
            "confirmed": "bg-success",
            "cancelled": "bg-danger",
            "completed": "bg-secondary",
        }

        return badge_classes.get(self.status, "bg-secondary")