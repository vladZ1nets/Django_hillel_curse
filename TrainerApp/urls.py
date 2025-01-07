from django.contrib import admin
from django.urls import path, include

import users.views
import trainer.views
import booking.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", include("users.urls")),
    path("login/", users.views.login_page, name="user_login"),
    path("logout/", users.views.logout_page, name="user_logout"),
    path("register/", users.views.register_page, name="user_register"),
    path("register/trainer/", trainer.views.trainer_registration, name="trainer_registration"),
    path("trainer/", include("trainer.urls")),
    path("category/", trainer.views.category_page, name="trainer_category"),
    path("service/", trainer.views.service_page, name="trainer_service"),
    path("userbook/", trainer.views.booking_for_user, name="booking_for_user"),
    path("booking/", include("booking.urls")),
]
