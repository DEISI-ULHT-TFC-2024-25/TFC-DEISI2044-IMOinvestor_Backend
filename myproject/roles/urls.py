# roles/urls.py

from django.urls import path
from .views import create_role

urlpatterns = [
    path('create/', create_role, name='create-role'),
]
