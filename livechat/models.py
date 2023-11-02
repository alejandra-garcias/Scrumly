from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    owner = models.ManyToManyField(User,
                                blank=True)
    is_private = models.BooleanField(default=False)
    room_code = models.CharField(max_length=1000,null=True,blank=True)
    def __str__(self):
        return self.name
    



class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000)
    room = models.CharField(max_length=1000)