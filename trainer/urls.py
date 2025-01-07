from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.category_page, name="category_page"),
    path("<int:trainer_id>/", views.trainer_page, name="trainer_page"),
    path("<int:trainer_id>/<int:service_id>/", views.trainer_service_page, name="trainer_service_page"),
    path("<int:trainer_id>/<int:service_id>/booking/", views.booking_for_user, name="booking_for_user"),
    path("register/", views.trainer_registration, name="trainer_registration"),
    path("services/", views.service_page, name="service_page"),
]
