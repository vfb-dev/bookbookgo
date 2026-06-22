from django import forms
from .models import Appointment


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
            "appointment_time": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        if appointment_date and appointment_time:
            appointment_exists = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            ).exists()

            if appointment_exists:
                raise forms.ValidationError(
                    "This appointment time is already booked. Please choose another time."
                )

        return cleaned_data