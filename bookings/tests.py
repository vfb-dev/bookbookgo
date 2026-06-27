from datetime import time, timedelta

from django.core import mail
from django.test import TestCase
from django.test import override_settings
from django.utils import timezone

from .emails import (
    send_accountant_new_appointment_email,
    send_client_appointment_received_email,
    send_client_status_update_email,
)
from .forms import AppointmentForm
from .models import Appointment, AvailabilityRule, BlockedDate, Service

# Create your tests here.
class AppointmentFormTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Tax Consultation",
            description="Tax help",
            duration_minutes=60,
            price=120,
            is_active=True,
        )

    def valid_form_data(self, **overrides):
        future_date = timezone.localdate() + timedelta(days=1)

        while future_date.weekday() >= 5:
            future_date += timedelta(days=1)

        data = {
            "service": self.service.id,
            "appointment_date": future_date,
            "appointment_time": time(9, 0),
            "full_name": "Victor Farias",
            "email": "victor@example.com",
            "phone": "21999999999",
            "business_name": "Car Shop",
            "business_type": "small_business",
            "message": "Need tax help.",
        }

        data.update(overrides)
        return data

    def test_valid_form_data_is_valid(self):
        form = AppointmentForm(data=self.valid_form_data())

        self.assertTrue(form.is_valid())

    def test_past_date_is_invalid(self):
        form = AppointmentForm(
            data=self.valid_form_data(
                appointment_date=timezone.localdate() - timedelta(days=1)
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("appointment_date", form.errors)

    def test_weekend_date_is_invalid(self):
        weekend_date = timezone.localdate()

        while weekend_date.weekday() < 5:
            weekend_date += timedelta(days=1)

        form = AppointmentForm(
            data=self.valid_form_data(appointment_date=weekend_date)
        )

        self.assertFalse(form.is_valid())
        self.assertIn("appointment_date", form.errors)

    def test_duplicate_time_slot_is_invalid(self):
        data = self.valid_form_data()

        Appointment.objects.create(
            service=self.service,
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            full_name="Existing Client",
            email="existing@example.com",
            phone="21111111111",
            business_name="Existing Co",
            business_type="small_business",
            message="Already booked.",
        )

        form = AppointmentForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("appointment_time", form.errors)

    def test_cancelled_time_slot_can_be_reused(self):
        data = self.valid_form_data()

        Appointment.objects.create(
            service=self.service,
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            full_name="Cancelled Client",
            email="cancelled@example.com",
            phone="21111111111",
            business_name="Cancelled Co",
            business_type="small_business",
            message="Cancelled booking.",
            status="cancelled",
        )

        form = AppointmentForm(data=data)

        self.assertTrue(form.is_valid())

    def test_blocked_date_is_invalid(self):
        data = self.valid_form_data()
        BlockedDate.objects.create(
            date=data["appointment_date"],
            reason="Holiday",
        )

        form = AppointmentForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("appointment_date", form.errors)

    def test_saturday_can_be_available_with_rule(self):
        saturday = timezone.localdate()

        while saturday.weekday() != 5:
            saturday += timedelta(days=1)

        AvailabilityRule.objects.create(
            weekday=5,
            start_time=time(9, 0),
            end_time=time(12, 0),
            slot_duration_minutes=60,
            is_active=True,
        )

        form = AppointmentForm(data=self.valid_form_data(appointment_date=saturday))

        self.assertTrue(form.is_valid())

    def test_inactive_services_are_not_in_form_queryset(self):
        inactive_service = Service.objects.create(
            name="Inactive Service",
            duration_minutes=60,
            price=100,
            is_active=False,
        )

        form = AppointmentForm()

        self.assertIn(self.service, form.fields["service"].queryset)
        self.assertNotIn(inactive_service, form.fields["service"].queryset)


class ContactPageTests(TestCase):
    def test_contact_page_loads(self):
        response = self.client.get("/contact/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/contact.html")
        self.assertContains(response, "+1 (555) 016-2040")
        self.assertContains(response, "hello@bookbookgo.com")
        self.assertContains(response, "Instagram")


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="BookBookGo <bookings@example.com>",
    ACCOUNTANT_EMAIL="accountant@example.com",
    SUPPORT_EMAIL="support@example.com",
    BUSINESS_NAME="BookBookGo",
    SITE_URL="https://bookbookgo.example",
)
class AppointmentEmailTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Tax Consultation",
            description="Tax help",
            duration_minutes=60,
            price=120,
            is_active=True,
        )
        self.appointment = Appointment.objects.create(
            service=self.service,
            appointment_date=timezone.localdate() + timedelta(days=1),
            appointment_time=time(9, 0),
            full_name="Victor Farias",
            email="victor@example.com",
            phone="21999999999",
            business_name="Car Shop",
            business_type="small_business",
            message="Need tax help.",
        )

    def test_client_received_email_is_multipart_and_links_to_booking(self):
        send_client_appointment_received_email(self.appointment)

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, "We received your appointment request")
        self.assertEqual(message.to, ["victor@example.com"])
        self.assertEqual(message.reply_to, ["support@example.com"])
        self.assertIn("View or manage your appointment", message.body)
        self.assertIn("https://bookbookgo.example/booking/success/", message.body)
        self.assertEqual(message.alternatives[0][1], "text/html")
        self.assertIn("View or manage appointment", message.alternatives[0][0])

    def test_accountant_email_goes_to_accountant_and_replies_to_client(self):
        send_accountant_new_appointment_email(self.appointment)

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(
            message.subject,
            "New appointment request from Victor Farias",
        )
        self.assertEqual(message.to, ["accountant@example.com"])
        self.assertEqual(message.reply_to, ["victor@example.com"])
        self.assertIn("Need tax help.", message.body)

    def test_status_update_email_uses_status_specific_copy(self):
        self.appointment.status = "confirmed"
        self.appointment.save(update_fields=["status", "updated_at"])

        send_client_status_update_email(self.appointment)

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, "Your appointment is confirmed")
        self.assertIn("Your accounting consultation has been confirmed.", message.body)
