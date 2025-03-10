from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer

class PropertyCreateView(APIView):
    def post(self, request):
        # Create a new property using the provided data
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            # Save the property to the database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
