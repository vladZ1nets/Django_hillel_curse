from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_page, name="user_page"),
    path("<user_id>", views.specific_user, name="specific_user"),
]