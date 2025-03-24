from django.urls import path
from .views import PropertyCreateView

urlpatterns = [
    path('create/', PropertyCreateView.as_view(), name='add-property'),
]
