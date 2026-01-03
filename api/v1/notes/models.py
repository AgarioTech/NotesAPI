import datetime

from django.utils import timezone
from django.db import models

from api.v1.users.models import CustomUser


# Create your models here.
class Note\
            (models.Model):
    title = models.CharField()
    description = models.TextField()
    date = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notes')
