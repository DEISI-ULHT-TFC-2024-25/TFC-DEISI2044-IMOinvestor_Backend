# duser/views.py
from rest_framework import status, generics,permissions
from rest_framework.response import Response
from .models import DUser
from .serializers import DUserSerializer

from rest_framework.views import APIView
from .serializers import LoginSerializer

from .serializers import UpdateUserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated



class CreateUserView(generics.CreateAPIView):
    queryset = DUser.objects.all()
    serializer_class = DUserSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateUserView(APIView):

    def put(self, request):
        # Extract user_id from the request body
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_instance = DUser.objects.get(id=user_id)
        except DUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Use the serializer to validate and update the instance
        serializer = UpdateUserSerializer(user_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)