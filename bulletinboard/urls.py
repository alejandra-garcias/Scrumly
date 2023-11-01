from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.bulletinboard), name='bulletinboard'),
    path('post/<str:pk>', views.post, name='post')]