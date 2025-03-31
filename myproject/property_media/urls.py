from django.urls import path
from .views import PropertyMediaCreateView

urlpatterns = [
    path('create/', PropertyMediaCreateView.as_view(), name='create-property-media'),
]
