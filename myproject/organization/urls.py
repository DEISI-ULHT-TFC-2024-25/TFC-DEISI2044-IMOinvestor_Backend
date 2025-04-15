from django.urls import path
from .views import*

urlpatterns = [
    path("create/", OrganizationCreateView.as_view(), name="create-organization"),
    path("list/", OrganizationListView.as_view(), name="list-organizations"),  # GET público
]
