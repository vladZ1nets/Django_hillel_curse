from trainer.utils import booking_time_discovery
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from trainer.models import Category, Service
from booking.models import Booking
import datetime


class TrainerAppTests(TestCase):

    def setUp(self):
        # Створення груп
        self.trainer_group = Group.objects.create(name="Trainer")
        self.client_group = Group.objects.create(name="Client")

        # Створення користувачів
        self.trainer_user = User.objects.create_user(
            username="trainer_user",
            password="trainerpass",
            email="trainer@example.com"
        )
        self.trainer_user.groups.add(self.trainer_group)
        self.trainer_user.save()

        self.client_user = User.objects.create_user(
            username="client_user",
            password="clientpass",
            email="client@example.com"
        )
        self.client_user.groups.add(self.client_group)
        self.client_user.save()

        # Створення категорій
        self.category1 = Category.objects.create(name="Фітнес")
        self.category2 = Category.objects.create(name="Йога")

        # Створення послуг
        self.service1 = Service.objects.create(
            trainer=self.trainer_user,
            category=self.category1,
            price=100,
            duration=60,
            level=1
        )
        self.service2 = Service.objects.create(
            trainer=self.trainer_user,
            category=self.category2,
            price=150,
            duration=45,
            level=2
        )

    # Тест на перегляд всіх категорій
    def test_view_all_categories(self):
        response = self.client.get(reverse('category_page'))  # Замість category_page — реальна назва вашого виду
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Фітнес")
        self.assertContains(response, "Йога")

    # Тест для перегляду сторінки тренера (для тренерів)
    def test_trainer_page_shows_services(self):
        self.client.login(username='trainer_user', password='trainerpass')
        response = self.client.get(reverse('trainer_page', args=[self.trainer_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Фітнес")
        self.assertContains(response, "Йога")


    # Тест для перевірки доступу до сторінки додавання послуги для не тренера
    def test_non_trainer_add_service(self):
        self.client.login(username="client_user", password="clientpass")

        # Спроба додати послугу
        response = self.client.post(reverse('service_page'), {
            'category': self.category1.id,
            'price': 100,
            'duration': 60,
            'level': 1
        })

        self.assertEqual(response.status_code, 403)



class TestSchedule(TestCase):
    maxDiff = None

    def test_schedule_no_bookings(self):
        schedule_start = datetime.datetime(2024, 12, 25, 9, 0)
        schedule_end = datetime.datetime(2024, 12, 25, 14, 0)
        trainer_bookings = []
        search_window = 60
        results = booking_time_discovery(schedule_start, schedule_end, trainer_bookings, search_window)
        expected = [
            datetime.datetime(2024, 12, 25, 9, 0), datetime.datetime(2024, 12, 25, 9, 15), datetime.datetime(2024, 12, 25, 9, 30), datetime.datetime(2024, 12, 25, 9, 45),
            datetime.datetime(2024, 12, 25, 10, 0), datetime.datetime(2024, 12, 25, 10, 15), datetime.datetime(2024, 12, 25, 10, 30), datetime.datetime(2024, 12, 25, 10, 45),
            datetime.datetime(2024, 12, 25, 11, 0), datetime.datetime(2024, 12, 25, 11, 15), datetime.datetime(2024, 12, 25, 11, 30), datetime.datetime(2024, 12, 25, 11, 45),
            datetime.datetime(2024, 12, 25, 12, 0), datetime.datetime(2024, 12, 25, 12, 15), datetime.datetime(2024, 12, 25, 12, 30), datetime.datetime(2024, 12, 25, 12, 45),
            datetime.datetime(2024, 12, 25, 13, 0)
        ]
        self.assertListEqual(expected, results)

        search_window = 30
        expected = [
            datetime.datetime(2024, 12, 25, 9, 0), datetime.datetime(2024, 12, 25, 9, 15),
            datetime.datetime(2024, 12, 25, 9, 30), datetime.datetime(2024, 12, 25, 9, 45),
            datetime.datetime(2024, 12, 25, 10, 0), datetime.datetime(2024, 12, 25, 10, 15),
            datetime.datetime(2024, 12, 25, 10, 30), datetime.datetime(2024, 12, 25, 10, 45),
            datetime.datetime(2024, 12, 25, 11, 0), datetime.datetime(2024, 12, 25, 11, 15),
            datetime.datetime(2024, 12, 25, 11, 30), datetime.datetime(2024, 12, 25, 11, 45),
            datetime.datetime(2024, 12, 25, 12, 0), datetime.datetime(2024, 12, 25, 12, 15),
            datetime.datetime(2024, 12, 25, 12, 30), datetime.datetime(2024, 12, 25, 12, 45),
            datetime.datetime(2024, 12, 25, 13, 0), datetime.datetime(2024, 12, 25, 13, 15),
            datetime.datetime(2024, 12, 25, 13, 30)
        ]
        results = booking_time_discovery(schedule_start, schedule_end, trainer_bookings, search_window)
        self.assertListEqual(expected, results)

    def test_schedule_one_booking(self):
        start_date = datetime.datetime(2024, 12, 25, 9, 0)
        end_date = datetime.datetime(2024, 12, 25, 14, 0)
        search_window = 60
        trainer_bookings = [
            (datetime.datetime(2024, 12, 25, 10, 0), datetime.datetime(2024, 12, 25, 11, 0),),
        ]
        results = booking_time_discovery(start_date, end_date, trainer_bookings, search_window)
        expected = [
            datetime.datetime(2024, 12, 25, 9, 0),
            datetime.datetime(2024, 12, 25, 11, 0),
            datetime.datetime(2024, 12, 25, 11, 15),
            datetime.datetime(2024, 12, 25, 11, 30),
            datetime.datetime(2024, 12, 25, 11, 45),
            datetime.datetime(2024, 12, 25, 12, 0),
            datetime.datetime(2024, 12, 25, 12, 15),
            datetime.datetime(2024, 12, 25, 12, 30),
            datetime.datetime(2024, 12, 25, 12, 45),
            datetime.datetime(2024, 12, 25, 13, 0)
        ]
        self.assertListEqual(expected, results)

        # Тест для пошуку вікон 30 хвилин
        search_window = 30
        expected = [
            datetime.datetime(2024, 12, 25, 9, 0), datetime.datetime(2024, 12, 25, 9, 15),
            datetime.datetime(2024, 12, 25, 9, 30),
            datetime.datetime(2024, 12, 25, 11, 0), datetime.datetime(2024, 12, 25, 11, 15),
            datetime.datetime(2024, 12, 25, 11, 30), datetime.datetime(2024, 12, 25, 11, 45),
            datetime.datetime(2024, 12, 25, 12, 0), datetime.datetime(2024, 12, 25, 12, 15),
            datetime.datetime(2024, 12, 25, 12, 30), datetime.datetime(2024, 12, 25, 12, 45),
            datetime.datetime(2024, 12, 25, 13, 0), datetime.datetime(2024, 12, 25, 13, 15),
            datetime.datetime(2024, 12, 25, 13, 30)
        ]
        results = booking_time_discovery(start_date, end_date, trainer_bookings, search_window)
        self.assertListEqual(expected, results)

        # Тест для різних бронювань
        search_window = 60
        trainer_bookings = [
            (datetime.datetime(2024, 12, 25, 9, 0), datetime.datetime(2024, 12, 25, 10, 0),),
        ]
        expected = [
            datetime.datetime(2024, 12, 25, 10, 0), datetime.datetime(2024, 12, 25, 10, 15),
            datetime.datetime(2024, 12, 25, 10, 30), datetime.datetime(2024, 12, 25, 10, 45),
            datetime.datetime(2024, 12, 25, 11, 0), datetime.datetime(2024, 12, 25, 11, 15),
            datetime.datetime(2024, 12, 25, 11, 30), datetime.datetime(2024, 12, 25, 11, 45),
            datetime.datetime(2024, 12, 25, 12, 0), datetime.datetime(2024, 12, 25, 12, 15),
            datetime.datetime(2024, 12, 25, 12, 30), datetime.datetime(2024, 12, 25, 12, 45),
            datetime.datetime(2024, 12, 25, 13, 0)
        ]
        results = booking_time_discovery(start_date, end_date, trainer_bookings, search_window)
        self.assertListEqual(expected, results)

        # Тест для додаткового бронювання в другій частині дня
        search_window = 60
        trainer_bookings = [
            (datetime.datetime(2024, 12, 25, 13, 0), datetime.datetime(2024, 12, 25, 14, 0),),
        ]
        expected = [
            datetime.datetime(2024, 12, 25, 9, 0), datetime.datetime(2024, 12, 25, 9, 15),
            datetime.datetime(2024, 12, 25, 9, 30), datetime.datetime(2024, 12, 25, 9, 45),
            datetime.datetime(2024, 12, 25, 10, 0), datetime.datetime(2024, 12, 25, 10, 15),
            datetime.datetime(2024, 12, 25, 10, 30), datetime.datetime(2024, 12, 25, 10, 45),
            datetime.datetime(2024, 12, 25, 11, 0), datetime.datetime(2024, 12, 25, 11, 15),
            datetime.datetime(2024, 12, 25, 11, 30), datetime.datetime(2024, 12, 25, 11, 45),
            datetime.datetime(2024, 12, 25, 12, 0)
        ]
        results = booking_time_discovery(start_date, end_date, trainer_bookings, search_window)
        self.assertListEqual(expected, results)

    def test_schedule_two_bookings(self):
        start_date = datetime.datetime(2024, 12, 25, 9, 0)
        end_date = datetime.datetime(2024, 12, 25, 14, 0)
        search_window = 60
        trainer_bookings = [
            (datetime.datetime(2024, 12, 25, 10, 0), datetime.datetime(2024, 12, 25, 11, 0),),
            (datetime.datetime(2024, 12, 25, 12, 0), datetime.datetime(2024, 12, 25, 13, 0),),
        ]

        expected = [datetime.datetime(2024, 12, 25, 9, 0),
                    datetime.datetime(2024, 12, 25, 11, 0),
                    datetime.datetime(2024, 12, 25, 13, 0)]
        results = booking_time_discovery(start_date, end_date, trainer_bookings, search_window)
        self.assertListEqual(expected, results)


