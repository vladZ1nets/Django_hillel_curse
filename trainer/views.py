import datetime
from dateutil import parser
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
import trainer.models
from trainer.utils import booking_time_discovery
import booking.models as booking_models
from users.models import User as CustomUser
from users.forms import RegisterForm
def category_page(request):
    service_categories = trainer.models.Category.objects.all()
    return render(request, "categories.html", {"categories": service_categories})

def trainer_page(request, trainer_id):
    if request.user.groups.filter(name='Trainer').exists():
        if request.method == "GET":
            service_categories = trainer.models.Category.objects.all()
            my_services = trainer.models.Service.objects.filter(trainer=request.user).all()
            return render(request,"trainer.html", {"categories": service_categories, "services": my_services})
    else:
        trainer_model = User.objects.get(id=trainer_id)
        trainer_data = trainer.models.TrainerDescription.objects.filter(trainer=trainer_model)
        trainer_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=trainer_model)
        return render(request, 'account.html', context={'trainer_data': trainer_data, "trainer_schedule": trainer_schedule})

def trainer_service_page(request, trainer_id, service_id):
    current_trainer = User.objects.get(id=trainer_id)
    specific_service = trainer.models.Service.objects.get(id=service_id)
    if request.method == "GET":
        available_times = []
        days_from_now = 1
        today = datetime.now()
        while days_from_now <= 7:
            cur_date = datetime(today.year, today.month, today.day) + datetime.timedelta(days=days_from_now)
            # Отримуємо список бронювань для цього дня
            training_bookings = booking_models.Booking.objects.filter(trainer=current_trainer,
                                                                      datetime_start__date=cur_date.date()).all()
            bookings_list = [(itm.datetime_start, itm.datetime_end) for itm in training_bookings]
            # Отримуємо графік тренування на цей день
            training_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=current_trainer,
                                                                              datetime_start__date=cur_date.date())
            for schedule in training_schedule:
                available_times += booking_time_discovery(schedule.datetime_start, schedule.datetime_end, bookings_list,
                                                          search_window=30)
            days_from_now += 1
        return render(request, 'trainer_service_page.html',
                      context={'specific_service': specific_service, 'available_times': available_times})
    else:
        # Обробка POST запиту
        booking_start = parser.parse(request.POST.get('training-start'))
        current_user = User.objects.get(id=current_trainer.id)
        booking_models.Booking.objects.create(trainer=current_trainer, user=current_user, service=specific_service,
                                              datetime_start=booking_start,
                                              datetime_end=booking_start + datetime.timedelta(minutes=specific_service.duration))
    return HttpResponse("Hello, world. You're at the polls index.")

def service_page(request):
    if request.method == "GET":
        services = trainer.models.Service.objects.all()
        return render(request, "services.html", context={"services":services})
    else:
        if request.user.groups.filter(name='Trainer').exists():
            form_data = request.POST
            service_cat = trainer.models.Category.objects.get(pk=form_data["category"])
            service = trainer.models.Service(
                level = form_data["level"],
                duration = form_data["duration"],
                price = form_data["price"],
                trainer = request.user,
                category = service_cat
            )
            service.save()
            return redirect(f'/trainer/{request.user.id}')
        else:
            return HttpResponseForbidden("You don't have permission to add services.")
def booking_for_user(request):
    if request.user.is_authenticated:
        user_bookings = booking_models.Booking.objects.filter(user=request.user)
        return render(request, "user_bookings.html", {"bookings": user_bookings})
    return HttpResponse("You need to login first")

def trainer_registration(request):
    if request.method == "GET":
        trainer_signup_form = RegisterForm()
        context = {"trainer_signup_form": trainer_signup_form}
        return render(request, "trainer_signup.html", context=context)
    else:
        trainer_signup_form = RegisterForm(request.POST)
        if trainer_signup_form.is_valid():
            trainer_group = Group.objects.get(name="Trainer")
            created_user = trainer_signup_form.save()
            created_user.groups.add(trainer_group)
            trainer_signup_form.save()
        return render(request, 'login.html')
