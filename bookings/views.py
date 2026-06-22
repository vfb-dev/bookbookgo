from django.shortcuts import render
from django.views import View

# Create your views here.
class AppointmentCreateView(View):
    def get(self, request):
        return render(request, "bookings/appointment_form.html")