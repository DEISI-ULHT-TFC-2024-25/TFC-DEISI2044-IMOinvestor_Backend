# duser/urls.py
from django.urls import path
from .views import*

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path("login/", LoginView.as_view(), name="login"),
    path('update/', UpdateUserView.as_view(), name='update-user'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('<int:id>/delete/', UserDeleteView.as_view(), name='user-delete'),

]
