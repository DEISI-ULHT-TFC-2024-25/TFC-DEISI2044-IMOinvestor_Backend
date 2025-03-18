# duser/urls.py
from django.urls import path
from .views import CreateUserView, LoginView, UpdateUserView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path("login/", LoginView.as_view(), name="login"),
    path('update/', UpdateUserView.as_view(), name='update-user'),

]
