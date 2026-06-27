import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags


logger = logging.getLogger(__name__)


def appointment_public_url(appointment):
    path = reverse(
        "appointment_success",
        kwargs={"token": appointment.public_token},
    )
    site_url = getattr(settings, "SITE_URL", "").rstrip("/")

    if site_url:
        return f"{site_url}{path}"

    return path


def appointment_context(appointment):
    return {
        "appointment": appointment,
        "appointment_url": appointment_public_url(appointment),
        "business_name": getattr(settings, "BUSINESS_NAME", "BookBookGo"),
        "support_email": getattr(settings, "SUPPORT_EMAIL", settings.ACCOUNTANT_EMAIL),
    }


def send_templated_email(
    *,
    subject,
    template_name,
    context,
    recipient_list,
    reply_to=None,
):
    html_body = render_to_string(f"emails/{template_name}.html", context)
    text_body = render_to_string(f"emails/{template_name}.txt", context).strip()

    if not text_body:
        text_body = strip_tags(html_body)

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
        reply_to=reply_to or [getattr(settings, "SUPPORT_EMAIL", settings.ACCOUNTANT_EMAIL)],
    )
    message.attach_alternative(html_body, "text/html")

    try:
        return message.send(fail_silently=False)
    except Exception:
        logger.exception("Could not send email: %s", subject)
        return 0


def send_client_appointment_received_email(appointment):
    return send_templated_email(
        subject="We received your appointment request",
        template_name="client_appointment_received",
        context=appointment_context(appointment),
        recipient_list=[appointment.email],
    )


def send_accountant_new_appointment_email(appointment):
    return send_templated_email(
        subject=f"New appointment request from {appointment.full_name}",
        template_name="accountant_new_appointment",
        context=appointment_context(appointment),
        recipient_list=[settings.ACCOUNTANT_EMAIL],
        reply_to=[appointment.email],
    )


def send_client_status_update_email(appointment):
    if appointment.status == "confirmed":
        subject = "Your appointment is confirmed"
        status_intro = "Your accounting consultation has been confirmed."
        status_detail = "We look forward to speaking with you."
    elif appointment.status == "cancelled":
        subject = "Your appointment was cancelled"
        status_intro = "Your accounting consultation has been cancelled."
        status_detail = "If this was a mistake, you can book a new appointment anytime."
    else:
        subject = f"Your appointment is {appointment.get_status_display().lower()}"
        status_intro = (
            f"Your appointment status is now "
            f"{appointment.get_status_display().lower()}."
        )
        status_detail = "Thank you for keeping your booking up to date."

    context = appointment_context(appointment)
    context.update(
        {
            "status_intro": status_intro,
            "status_detail": status_detail,
        }
    )

    return send_templated_email(
        subject=subject,
        template_name="client_status_update",
        context=context,
        recipient_list=[appointment.email],
    )
