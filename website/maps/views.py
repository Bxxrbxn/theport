from django.shortcuts import render
from .models import PaymentRecord

def map_view(request):
    return render(request, 'map.html', {'AIzaSyAgekxD1j7QjNQDhAO1MO6xJYFkgajc7x4': settings.GOOGLE_MAPS_API_KEY})

def payment_list(request):
    records = PaymentRecord.objects.all()
    return render(request, 'user_main.html', {'records': records})