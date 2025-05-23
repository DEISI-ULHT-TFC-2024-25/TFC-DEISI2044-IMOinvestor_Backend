from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyMediaViewSet

router = DefaultRouter()
router.register(r'', PropertyMediaViewSet, basename='property-media')

urlpatterns = [
    path('', include(router.urls)),
]
