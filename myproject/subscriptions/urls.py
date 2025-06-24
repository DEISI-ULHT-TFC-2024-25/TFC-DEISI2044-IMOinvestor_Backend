# subscriptions/urls.py
from django.urls import path
from .views import UpdateSubscriptionView

urlpatterns = [
    path('update/', UpdateSubscriptionView.as_view(), name='update-subscription'),
]
