from django.urls import path
from user import views

urlpatterns = [
    path("signup", views.usersignup, name="usersignup"),
    path("verify_otp", views.verify_otp, name="verify_otp"),
    path("login", views.userlogin, name="userlogin"),
    path("logout", views.userlogout, name="userlogout"),
    path('current_user', views.current_user, name='current_user'),

]
