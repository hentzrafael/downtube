from django.urls import path
from . import views

urlpatterns = [
    path('download', views.details, name='details'),
    path('', views.index, name='index'),
]