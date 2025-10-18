from django.urls import path
from . import views

urlpatterns = [
    path("create_multiple/", views.create_multiple_payment, name="create_multiple_payment"),
    path("verify/<str:order_id>/", views.verify_payment, name="verify_payment"), 
]