from django.urls import path,include
from .views import AnnouncementCreateView,AnnouncementViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'filter', AnnouncementViewSet, basename='announcement')


urlpatterns = [
    path("create/", AnnouncementCreateView.as_view(), name="create"),
    path("", include(router.urls)),  # Includes the announcement listing with filtering

]
