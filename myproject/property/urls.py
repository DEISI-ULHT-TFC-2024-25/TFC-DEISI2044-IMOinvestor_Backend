from django.urls import path
from .views import PropertyCreateView

urlpatterns = [
    path('add/', PropertyCreateView.as_view(), name='add-property'),
]
