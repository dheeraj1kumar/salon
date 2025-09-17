from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("update/<int:booking_id>/<str:status>/", views.update_booking_status, name="update_booking_status"),
]
