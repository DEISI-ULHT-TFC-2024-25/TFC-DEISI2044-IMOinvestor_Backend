# duser/views.py
from rest_framework import status, generics,permissions
from rest_framework.response import Response
from .models import DUser
from .serializers import DUserSerializer

from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token



from .serializers import UpdateUserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .dtos import CreateUserDTO



class CreateUserView(APIView):

    @swagger_auto_schema(request_body=CreateUserDTO, responses={201: DUserSerializer})
    def post(self, request):

        dto = CreateUserDTO(data=request.data)
        if not dto.is_valid():
            return Response(dto.errors, status=status.HTTP_400_BAD_REQUEST)

        # Convert phone_number to string explicitly
        data = dict(dto.validated_data)
        data['phone_number'] = str(data['phone_number'])
        serializer = DUserSerializer(data=data) 

        if serializer.is_valid():
            user = serializer.save()
            return Response(DUserSerializer(user).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):   
        # Serialize the incoming data
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Return JWT tokens if the data is valid
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        # Return validation errors if not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''''
class LoginView(APIView):
    queryset = DUser.objects.all()
    serializer_class = DUserSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
'''
class UpdateUserView(APIView):

    @swagger_auto_schema(request_body=UpdateUserSerializer)

    def put(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_instance = DUser.objects.get(id=user_id)
        except DUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateUserSerializer(user_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)