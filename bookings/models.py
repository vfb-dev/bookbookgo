from django.db import models

# Create your models here.
class Appointment(models.Model):
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

    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    business_name = models.CharField(max_length=120, blank=True)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)