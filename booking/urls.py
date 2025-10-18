from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/<int:service_id>/", views.add_to_cart, name="add_to_cart"),
    path("item/<int:item_id>/remove/", views.remove_from_cart, name="remove_from_cart"),
    path("item/<int:item_id>/update/", views.update_cart_item, name="update_cart_item"),
    path("confirm/", views.confirm_booking, name="confirm_booking"),
    path("slots/", views.slots_api, name="slots_api"),
]

