from django.urls import path
from . import views

urlpatterns = [
    path("", views.booking_page, name="booking_page"),
    path("<int:booking_id>/cancel/", views.booking_cancel, name="booking_cancel"),
    path("<int:booking_id>/accept/", views.booking_acception, name="booking_acception"),
]
