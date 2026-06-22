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
            "appointment_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "message": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")