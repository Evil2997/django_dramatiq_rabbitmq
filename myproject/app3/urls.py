# app3/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('start_all_tasks/', views.start_all_tasks, name='start_all_tasks'),

]
