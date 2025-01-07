from django.contrib import admin

# Register your models here.
from trainer.models import TrainerSchedule, TrainerDescription, Category, Service
admin.site.register(TrainerSchedule)
admin.site.register(TrainerDescription)
admin.site.register(Category)
admin.site.register(Service)
