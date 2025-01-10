from trainer.utils import booking_time_discovery
from django.contrib.auth.models import Group, User
from django.test import TestCase, Client
from trainer.models import Service
import datetime
from trainer.utils import booking_time_discovery


class TrainerTest(TestCase):
    fixtures = ['new_fixture2.json']

    def test_show_all_trainers(self):
        client = Client()
        response = client.get('/trainer/')
        self.assertEqual(response.status_code, 200)

    def test_all_services(self):
        client = Client()
        response = client.get('/services/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/services/?trainer_id=1')
        self.assertEqual(response.status_code, 200)

    def test_trainer_add_service(self):
        # анонімний користувач
        client = Client()
        response = client.post('/services/', {'category': 1, 'price': 100, 'duration': 100, 'level': 1})
        self.assertEqual(response.status_code, 403)

        # користувач
        user = User.objects.create_user(
            username="test_client_user1",
            password="1111",
            email="user1@gmail.com",
            first_name="john",
            last_name="dow",
        )
        user.groups.add(Group.objects.get(name="client"))
        user.save()
        client.login(username="test_client_user1", password="1111")
        response = client.post('/services/', {'category': 1, 'price': 100, 'duration': 100, 'level': 1})
        self.assertEqual(response.status_code, 403)

        # тренер
        trainer = User.objects.create_user(
            username="test_trainer",
            password="1111",
            email="trainer@gmail.com",
            first_name="Jane",
            last_name="Doe",
        )
        trainer.groups.add(Group.objects.get(name="Trainer"))
        trainer.save()
        client.login(username="test_trainer", password="1111")
        response = client.post('/services/', {'category': 1, 'price': 100, 'duration': 100, 'level': 1})
        self.assertEqual(response.status_code, 302)

        created_service = Service.objects.filter(trainer=trainer).first()  # фільтруємо по тренеру
        self.assertEqual(created_service.trainer.username, 'test_trainer')
        self.assertEqual(created_service.price, 100)

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


