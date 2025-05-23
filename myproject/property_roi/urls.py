from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ROICalculationViewSet

router = DefaultRouter()
router.register(r'', ROICalculationViewSet, basename='roi-calculation')

urlpatterns = [
    path('', include(router.urls)),
]
