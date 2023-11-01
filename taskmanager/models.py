from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    completed= models.BooleanField(default=False)
    priority= models.BooleanField(default=False)
    def __str__(self):
        return self.subject
    class Meta:
        ordering=['completed']   
# Create your models here.
class Chatbot(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f'{self.user.username}:{self.message}'