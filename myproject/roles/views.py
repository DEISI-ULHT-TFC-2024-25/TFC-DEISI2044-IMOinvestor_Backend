# roles/views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Role
from .serializers import RoleSerializer
from drf_yasg.utils import swagger_auto_schema  # 👈 Make sure to import this

@swagger_auto_schema(method='post', request_body=RoleSerializer)
@api_view(['POST'])
def create_role(request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
