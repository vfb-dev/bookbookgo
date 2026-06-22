from django.shortcuts import render, redirect
from django.views import View
from .forms import AppointmentForm

# Create your views here.
class AppointmentCreateView(View):
    def get(self, request):
        form = AppointmentForm()
        return render(request, "bookings/appointment_form.html", {"form": form})

    def post(self, request):
        form = AppointmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("appointment_create")

        return render(request, "bookings/appointment_form.html", {"form": form})