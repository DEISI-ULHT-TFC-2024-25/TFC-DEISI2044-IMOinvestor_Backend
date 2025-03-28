from django.shortcuts import render

# Create your views here.

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import PropertyMedia
from .serializers import PropertyMediaSerializer

class PropertyMediaCreateView(generics.CreateAPIView):
    queryset = PropertyMedia.objects.all()
    serializer_class = PropertyMediaSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        property_id = request.data.get('property')

        if not property_id:
            return Response({'error': 'Property ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        created_media = []
        for file in files:
            media_type = 'image' if file.content_type.startswith('image') else 'video'
            media_data = {'property': property_id, 'file': file, 'media_type': media_type}
            serializer = self.get_serializer(data=media_data)
            if serializer.is_valid():
                serializer.save()
                created_media.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_media, status=status.HTTP_201_CREATED)

class PropertyMediaListView(generics.ListAPIView):
    queryset = PropertyMedia.objects.all()
    serializer_class = PropertyMediaSerializer


