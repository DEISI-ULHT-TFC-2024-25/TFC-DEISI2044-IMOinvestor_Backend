# duser/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from .models import DUser
from .serializers import DUserSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = DUser.objects.all()
    serializer_class = DUserSerializer
