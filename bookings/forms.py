from django.utils import timezone

from django import forms
from .models import Appointment, Service


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "service",
            "appointment_date",
            "appointment_time",
            "full_name",
            "email",
            "phone",
            "business_name",
            "business_type",
            "message",
        ]

        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "appointment_time": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Tell us what you want to review, any deadlines, and useful business context.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["service"].queryset = Service.objects.filter(is_active=True)
        self.fields["appointment_date"].widget.attrs["min"] = timezone.localdate().isoformat()
        self.fields["full_name"].widget.attrs["placeholder"] = "Your full name"
        self.fields["email"].widget.attrs["placeholder"] = "you@example.com"
        self.fields["phone"].widget.attrs["placeholder"] = "(555) 123-4567"
        self.fields["business_name"].widget.attrs["placeholder"] = "Optional"

        for name, field in self.fields.items():
            if name in {"service", "appointment_time", "business_type"}:
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        if appointment_date and appointment_date < timezone.localdate():
            self.add_error(
                "appointment_date",
                "Please choose today or a future date."
            )

        if appointment_date and appointment_date.weekday() >= 5:
            self.add_error(
                "appointment_date",
                "Appointments are only available Monday through Friday."
            )

        if appointment_date and appointment_time:
            appointment_exists = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            ).exists()

            if appointment_exists:
                self.add_error(
                    "appointment_time",
                    "This appointment time is already booked. Please choose another time."
                )

        return cleaned_data
    
class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["status"]

        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
        }
