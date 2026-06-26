from datetime import datetime, timedelta

from django.utils import timezone

from django import forms
from .models import Appointment, AvailabilityRule, BlockedDate, Service


def get_available_time_choices(appointment_date, exclude_appointment=None):
    if not appointment_date:
        return []

    if BlockedDate.objects.filter(date=appointment_date).exists():
        return []

    rules = AvailabilityRule.objects.filter(
        weekday=appointment_date.weekday(),
        is_active=True,
    )

    if rules.exists():
        slots = []

        for rule in rules:
            current = datetime.combine(appointment_date, rule.start_time)
            end = datetime.combine(appointment_date, rule.end_time)
            step = timedelta(minutes=rule.slot_duration_minutes)

            while current + step <= end:
                slots.append(current.time())
                current += step
    elif appointment_date.weekday() < 5:
        slots = [value for value, _label in Appointment.TIME_CHOICES]
    else:
        slots = []

    booked_times = Appointment.objects.filter(
        appointment_date=appointment_date,
    ).exclude(status="cancelled")

    if exclude_appointment and exclude_appointment.pk:
        booked_times = booked_times.exclude(pk=exclude_appointment.pk)

    booked_times = set(booked_times.values_list("appointment_time", flat=True))
    open_slots = sorted(set(slots) - booked_times)

    return [(slot, slot.strftime("%I:%M %p").lstrip("0")) for slot in open_slots]


class AppointmentAvailabilityMixin:
    appointment_date_field = "appointment_date"
    appointment_time_field = "appointment_time"

    def configure_time_choices(self):
        appointment_date = self._selected_appointment_date()
        choices = get_available_time_choices(
            appointment_date,
            exclude_appointment=self.instance,
        )

        if not appointment_date:
            placeholder = "Select a date first"
        elif choices:
            placeholder = "Select a time"
        else:
            placeholder = "No available times"

        self.fields[self.appointment_time_field].widget = forms.Select(
            attrs={"class": "form-select"}
        )
        self.fields[self.appointment_time_field].choices = [("", placeholder)] + choices

    def _selected_appointment_date(self):
        field_name = self.appointment_date_field

        if self.is_bound:
            raw_date = self.data.get(self.add_prefix(field_name))

            if raw_date:
                if hasattr(raw_date, "weekday"):
                    return raw_date

                try:
                    return datetime.strptime(raw_date, "%Y-%m-%d").date()
                except ValueError:
                    return None

        return getattr(self.instance, field_name, None)

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get(self.appointment_date_field)
        appointment_time = cleaned_data.get(self.appointment_time_field)

        if appointment_date and appointment_date < timezone.localdate():
            self.add_error(
                self.appointment_date_field,
                "Please choose today or a future date."
            )

        if appointment_date and BlockedDate.objects.filter(date=appointment_date).exists():
            self.add_error(
                self.appointment_date_field,
                "Appointments are not available on this date."
            )

        if (
            appointment_date
            and appointment_date.weekday() >= 5
            and not AvailabilityRule.objects.filter(
                weekday=appointment_date.weekday(),
                is_active=True,
            ).exists()
        ):
            self.add_error(
                self.appointment_date_field,
                "Appointments are not available on this day."
            )

        if appointment_date and appointment_time:
            available_times = {
                value for value, _label in get_available_time_choices(
                    appointment_date,
                    exclude_appointment=self.instance,
                )
            }

            if appointment_time not in available_times:
                self.add_error(
                    self.appointment_time_field,
                    "This appointment time is not available. Please choose another time."
                )

        return cleaned_data


class AppointmentForm(AppointmentAvailabilityMixin, forms.ModelForm):
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

        self.configure_time_choices()
    

class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["status"]

        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class AppointmentRescheduleForm(AppointmentAvailabilityMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["appointment_date", "appointment_time"]

        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["appointment_date"].widget.attrs["min"] = timezone.localdate().isoformat()
        self.configure_time_choices()
