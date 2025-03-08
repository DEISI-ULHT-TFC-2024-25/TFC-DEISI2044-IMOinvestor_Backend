from django.urls import path
from .views import OrganizationCreateView

urlpatterns = [
    path("create/", OrganizationCreateView.as_view(), name="create-organization"),
]
