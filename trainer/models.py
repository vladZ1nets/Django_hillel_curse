from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class TrainerDescription(models.Model):
    text = models.TextField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)

class TrainerSchedule(models.Model):
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    price =models.FloatField()
    level = models.IntegerField()
    duration = models.IntegerField()