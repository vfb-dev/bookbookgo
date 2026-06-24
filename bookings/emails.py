from django.conf import settings
from django.core.mail import send_mail


def send_client_appointment_received_email(appointment):
    send_mail(
        subject="Your appointment request was received",
        message=(
            f"Hi {appointment.full_name},\n\n"
            f"We received your appointment request.\n\n"
            f"Service: {appointment.get_service_display()}\n"
            f"Date: {appointment.appointment_date}\n"
            f"Time: {appointment.appointment_time.strftime('%I:%M %p')}\n\n"
            "We will contact you after reviewing your request."
        ),
        from_email=None,
        recipient_list=[appointment.email],
        fail_silently=False,
    )

def send_accountant_new_appointment_email(appointment):
    send_mail(
        subject="New appointment request",
        message=(
            "A new appointment request has been submitted.\n\n"
            f"Client: {appointment.full_name}\n"
            f"Email: {appointment.email}\n"
            f"Phone: {appointment.phone}\n"
            f"Service: {appointment.get_service_display()}\n"
            f"Date: {appointment.appointment_date}\n"
            f"Time: {appointment.appointment_time.strftime('%I:%M %p')}\n"
            f"Business: {appointment.business_name or 'Not provided'}\n"
            f"Business type: {appointment.get_business_type_display()}\n\n"
            f"Message:\n{appointment.message or 'No message provided.'}"
        ),
        from_email=None,
        recipient_list=[settings.ACCOUNTANT_EMAIL],
        fail_silently=False,
    )

def send_client_status_update_email(appointment):
    if appointment.status == "confirmed":
        subject = "Your appointment has been confirmed"
        intro = (
            "Good news — your accounting consultation has been confirmed."
        )
        closing = "We look forward to speaking with you."
    elif appointment.status == "cancelled":
        subject = "Your appointment has been cancelled"
        intro = (
            "Your accounting consultation has been cancelled. "
            "If this was a mistake, please book another appointment."
        )
        closing = "Thank you for understanding."
    else:
        subject = f"Your appointment is {appointment.get_status_display()}"
        intro = (
            f"Your appointment status has been updated to "
            f"{appointment.get_status_display()}."
        )
        closing = "Thank you."

    send_mail(
        subject=subject,
        message=(
            f"Hi {appointment.full_name},\n\n"
            f"{intro}\n\n"
            f"Service: {appointment.get_service_display()}\n"
            f"Date: {appointment.appointment_date}\n"
            f"Time: {appointment.appointment_time.strftime('%I:%M %p')}\n\n"
            f"{closing}"
        ),
        from_email=None,
        recipient_list=[appointment.email],
        fail_silently=False,
    )