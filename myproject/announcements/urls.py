from django.urls import path
from .views import AnnouncementCreateView

urlpatterns = [
    path("create/", AnnouncementCreateView.as_view(), name="create"),
]
