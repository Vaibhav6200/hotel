from django.urls import path
from . import views


app_name = "hms"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("rooms/", views.our_rooms, name="rooms"),
    path("details/<int:room_id>/", views.room_detail, name="room_detail"),
]
