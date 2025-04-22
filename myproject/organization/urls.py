from django.urls import path
from .views import*

urlpatterns = [
    path("create/", OrganizationCreateView.as_view(), name="create-organization"),
    path("list/", OrganizationListView.as_view(), name="list-organizations"), 
    path('<int:id>/', OrganizationDetailView.as_view(), name='get-organization'),
    path('<int:id>/delete/', OrganizationDeleteView.as_view(), name='delete-organization'),
    path('<int:id>/update/', OrganizationUpdateView.as_view(), name='update-organization'),
]
