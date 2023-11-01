from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import Logueo,PaginaRegistro
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.index, name="index"),
    path("insert/", login_required(views.insert), name="insert"),
    path("update", login_required(views.update), name="update"),
    path("update/<int:task_id>", login_required(views.update_form), name="update_form"),
    path("delete/<int:task_id>", login_required(views.delete), name="delete"),
    path('login/', Logueo.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('registro/',PaginaRegistro.as_view(),name='registro'),
    path('search/', views.search, name='search')

]