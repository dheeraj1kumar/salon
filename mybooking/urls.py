
from django.urls import path
from mybooking import views

urlpatterns = [
    path('', views.my_bookings, name='my_bookings'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
