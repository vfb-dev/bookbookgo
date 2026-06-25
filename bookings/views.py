from datetime import timedelta

from .forms import AppointmentForm, AppointmentStatusForm
from .models import Appointment, Service
from .emails import (
    send_accountant_new_appointment_email,
    send_client_appointment_received_email,
    send_client_status_update_email
)

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


class HomeView(View):
    def get(self, request):
        services = Service.objects.filter(is_active=True)

        return render(
            request,
            "bookings/home.html",
            {"services": services},
        )
    
class ContactView(View):
    def get(self, request):
        contact_context = {
            "phones": [
                {
                    "label": "Main office",
                    "display": "+1 (555) 016-2040",
                    "href": "+15550162040",
                    "note": "Appointments and general questions",
                },
                {
                    "label": "Client support",
                    "display": "+1 (555) 018-3270",
                    "href": "+15550183270",
                    "note": "Existing bookings and rescheduling",
                },
            ],
            "emails": [
                {
                    "label": "General email",
                    "address": "hello@bookbookgo.com",
                    "note": "Questions before you book",
                },
                {
                    "label": "Support email",
                    "address": "support@bookbookgo.com",
                    "note": "Help with an appointment request",
                },
            ],
            "social_links": [
                {"name": "Instagram", "handle": "@bookbookgo", "url": "https://www.instagram.com/bookbookgo/"},
                {"name": "Facebook", "handle": "BookBookGo", "url": "https://www.facebook.com/bookbookgo/"},
                {"name": "LinkedIn", "handle": "BookBookGo", "url": "https://www.linkedin.com/company/bookbookgo/"},
            ],
            "office_hours": "Monday to Friday, 9:00 AM - 5:00 PM",
        }

        return render(request, "bookings/contact.html", contact_context)

class DashboardView(LoginRequiredMixin, View):
    login_url = "/admin/login/"

    def get(self, request):
        today = timezone.localdate()
        selected_status = request.GET.get("status", "")
        search_query = request.GET.get("q", "")
        date_filter = request.GET.get("date_filter", "upcoming")

        appointments = Appointment.objects.all()

        if date_filter == "today":
            appointments = appointments.filter(appointment_date=today)
        elif date_filter == "week":
            end_date = today + timedelta(days=7)
            appointments = appointments.filter(
                appointment_date__gte=today,
                appointment_date__lte=end_date,
            )
        elif date_filter == "month":
            appointments = appointments.filter(
                appointment_date__year=today.year,
                appointment_date__month=today.month,
            )
        elif date_filter == "all":
            appointments = appointments
        else:
            appointments = appointments.filter(appointment_date__gte=today)

        appointments = appointments.order_by("appointment_date", "appointment_time")

        if selected_status:
            appointments = appointments.filter(status=selected_status)

        if search_query:
            appointments = appointments.filter(
                Q(full_name__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(phone__icontains=search_query)
                | Q(business_name__icontains=search_query)
            )

        paginator = Paginator(appointments, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "total_appointments": Appointment.objects.count(),
            "pending_appointments": Appointment.objects.filter(status="pending").count(),
            "confirmed_appointments": Appointment.objects.filter(status="confirmed").count(),
            "upcoming_appointments": page_obj,
            "page_obj": page_obj,
            "selected_status": selected_status,
            "search_query": search_query,
            "date_filter": date_filter,
            "status_choices": Appointment.STATUS_CHOICES,
        }

        return render(request, "bookings/dashboard.html", context)

class AppointmentCreateView(View):
    def get(self, request):
        form = AppointmentForm()
        services = Service.objects.filter(is_active=True)

        return render(request, "bookings/appointment_form.html", {"form": form, "services": services})

    def post(self, request):
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save()
            
            send_client_appointment_received_email(appointment)
            send_accountant_new_appointment_email(appointment)

            return redirect("appointment_success", token=appointment.public_token)

        return render(request, "bookings/appointment_form.html", {"form": form, "services": Service.objects.filter(is_active=True)})
    
class AppointmentSuccessView(View):
    def get(self, request, token):
        appointment = get_object_or_404(Appointment, public_token=token)
        return render(
            request,
            "bookings/appointment_success.html",
            {"appointment": appointment},
        )
    
class AppointmentDetailView(LoginRequiredMixin, View):
    login_url = "/admin/login/"

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        status_form = AppointmentStatusForm(instance=appointment)

        return render(
            request,
            "bookings/appointment_detail.html",
            {
                "appointment": appointment,
                "status_form": status_form,
            },
        )

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        old_status = appointment.status

        status_form = AppointmentStatusForm(request.POST, instance=appointment)

        if status_form.is_valid():
            appointment = status_form.save()

            if appointment.status != old_status:
                if appointment.status in ["confirmed", "cancelled"]:
                    send_client_status_update_email(appointment)
                    messages.success(
                        request,
                        "Appointment status updated and client notified."
                    )
                else:
                    messages.success(
                        request,
                        "Appointment status updated."
                    )
            else:
                messages.info(request, "No status change was made.")

            return redirect("appointment_detail", pk=appointment.pk)

        return render(
            request,
            "bookings/appointment_detail.html",
            {
                "appointment": appointment,
                "status_form": status_form,
            },
        )
    
class BookedTimesView(View):
    def get(self, request):
        appointment_date = request.GET.get("date")

        booked_times = Appointment.objects.filter(
            appointment_date=appointment_date
        ).values_list("appointment_time", flat=True)

        data = [time.strftime("%H:%M:%S") for time in booked_times]

        return JsonResponse({"booked_times": data})