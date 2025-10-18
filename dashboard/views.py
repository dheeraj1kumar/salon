from django.shortcuts import render
from .models import Service
# Create your views here.
from booking.models import CartItem
from django.utils.timezone import localtime

def home(request):
    services = Service.objects.all()
    cart_ids = set(CartItem.objects.filter(user=request.user).values_list("service_id", flat=True)) if request.user.is_authenticated else set()
    return render(request, "home.html", {"services": services, "cart_ids": cart_ids})









