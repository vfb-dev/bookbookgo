from datetime import time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from bookings.models import Appointment, Service


class Command(BaseCommand):
    help = "Create demo services and appointments."

    def handle(self, *args, **options):
        services = [
            {
                "name": "Tax Consultation",
                "description": "Review tax questions and prepare next steps.",
                "duration_minutes": 60,
                "price": 120,
            },
            {
                "name": "Bookkeeping Setup",
                "description": "Set up a clean bookkeeping workflow for a small business.",
                "duration_minutes": 90,
                "price": 180,
            },
            {
                "name": "Payroll Review",
                "description": "Review payroll processes, compliance, and reporting.",
                "duration_minutes": 60,
                "price": 140,
            },
            {
                "name": "Business Finance Consultation",
                "description": "Discuss cash flow, expenses, and business planning.",
                "duration_minutes": 75,
                "price": 160,
            },
            {
                "name": "Personal Finance Consultation",
                "description": "Review budgeting, savings, and personal financial planning.",
                "duration_minutes": 60,
                "price": 100,
            },
            {
                "name": "Startup Advisory",
                "description": "Plan basic accounting, taxes, and cash flow for a new business.",
                "duration_minutes": 90,
                "price": 200,
            },
        ]

        created_services = []

        for service_data in services:
            service, _ = Service.objects.get_or_create(
                name=service_data["name"],
                defaults=service_data,
            )
            created_services.append(service)

        today = timezone.localdate()

        appointment_data = [
            {
                "service": created_services[0],
                "appointment_date": today + timedelta(days=1),
                "appointment_time": time(9, 0),
                "full_name": "Victor Farias",
                "email": "victor@example.com",
                "phone": "21999999999",
                "business_name": "Car Shop",
                "business_type": "small_business",
                "message": "Need help preparing business taxes.",
                "status": "pending",
            },
            {
                "service": created_services[1],
                "appointment_date": today + timedelta(days=1),
                "appointment_time": time(10, 0),
                "full_name": "Marina Souza",
                "email": "marina@example.com",
                "phone": "21888888888",
                "business_name": "Studio Azul",
                "business_type": "freelancer",
                "message": "I need a bookkeeping system for invoices and expenses.",
                "status": "confirmed",
            },
            {
                "service": created_services[2],
                "appointment_date": today + timedelta(days=2),
                "appointment_time": time(11, 0),
                "full_name": "Daniel Costa",
                "email": "daniel@example.com",
                "phone": "21777777777",
                "business_name": "Costa Services",
                "business_type": "llc_corp",
                "message": "Want to review payroll setup before hiring.",
                "status": "cancelled",
            },
            {
                "service": created_services[3],
                "appointment_date": today + timedelta(days=2),
                "appointment_time": time(13, 0),
                "full_name": "Ana Ribeiro",
                "email": "ana@example.com",
                "phone": "21666666666",
                "business_name": "Ribeiro Bakery",
                "business_type": "small_business",
                "message": "Need help understanding monthly expenses and profit.",
                "status": "confirmed",
            },
            {
                "service": created_services[4],
                "appointment_date": today + timedelta(days=3),
                "appointment_time": time(14, 0),
                "full_name": "Lucas Almeida",
                "email": "lucas@example.com",
                "phone": "21555555555",
                "business_name": "",
                "business_type": "individual",
                "message": "Looking for help organizing personal finances.",
                "status": "pending",
            },
            {
                "service": created_services[5],
                "appointment_date": today + timedelta(days=3),
                "appointment_time": time(15, 0),
                "full_name": "Bianca Martins",
                "email": "bianca@example.com",
                "phone": "21444444444",
                "business_name": "Martins Design Co.",
                "business_type": "freelancer",
                "message": "Starting a design studio and need accounting guidance.",
                "status": "completed",
            },
            {
                "service": created_services[0],
                "appointment_date": today + timedelta(days=4),
                "appointment_time": time(9, 0),
                "full_name": "Rafael Gomes",
                "email": "rafael@example.com",
                "phone": "21333333333",
                "business_name": "Gomes Auto Parts",
                "business_type": "small_business",
                "message": "Need tax planning before the next quarter.",
                "status": "pending",
            },
            {
                "service": created_services[1],
                "appointment_date": today + timedelta(days=4),
                "appointment_time": time(10, 0),
                "full_name": "Camila Rocha",
                "email": "camila@example.com",
                "phone": "21222222222",
                "business_name": "Rocha Fitness",
                "business_type": "small_business",
                "message": "Need bookkeeping organized for membership payments.",
                "status": "confirmed",
            },
            {
                "service": created_services[3],
                "appointment_date": today + timedelta(days=5),
                "appointment_time": time(13, 0),
                "full_name": "Felipe Nunes",
                "email": "felipe@example.com",
                "phone": "21111111111",
                "business_name": "Nunes Consulting",
                "business_type": "llc_corp",
                "message": "Need advice on cash flow and service pricing.",
                "status": "pending",
            },
            {
                "service": created_services[2],
                "appointment_date": today + timedelta(days=5),
                "appointment_time": time(16, 0),
                "full_name": "Juliana Barros",
                "email": "juliana@example.com",
                "phone": "21000000000",
                "business_name": "Barros Events",
                "business_type": "small_business",
                "message": "Need help reviewing payroll for event staff.",
                "status": "cancelled",
            },
        ]

        for data in appointment_data:
            Appointment.objects.get_or_create(
                appointment_date=data["appointment_date"],
                appointment_time=data["appointment_time"],
                defaults=data,
            )

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))