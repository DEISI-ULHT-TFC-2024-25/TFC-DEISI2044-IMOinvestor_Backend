from django.urls import path
from .views import*

urlpatterns = [
    path('create/', PropertyCreateView.as_view(), name='add-property'),
    path('', PropertyListView.as_view(), name='list-properties'),
    path('<int:id>/', PropertyDetailView.as_view(), name='get-property'),
    path('<int:id>/delete/', PropertyDeleteView.as_view(), name='delete-property'),
    path('<int:id>/update/', PropertyUpdateView.as_view(), name='update-property'),
    path('organization/<int:organization_id>/', PropertyByOrganizationView.as_view(), name='property-by-organization'),
]

