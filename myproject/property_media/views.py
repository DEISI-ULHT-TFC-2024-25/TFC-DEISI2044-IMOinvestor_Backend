from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import PropertyMedia
from .serializers import PropertyMediaSerializer
from rest_framework.exceptions import MethodNotAllowed

class PropertyMediaViewSet(viewsets.ModelViewSet):
    queryset = PropertyMedia.objects.all()
    serializer_class = PropertyMediaSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        property_id = self.request.query_params.get('property')
        if property_id:
            return PropertyMedia.objects.filter(property_id=property_id)
        return PropertyMedia.objects.all()

    @swagger_auto_schema(
        operation_summary="Create a new Property-media",
        manual_parameters=[
            openapi.Parameter('property', openapi.IN_FORM, description="ID da propriedade", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('file', openapi.IN_FORM, description="Arquivos de mídia (imagens ou vídeos)", type=openapi.TYPE_FILE, required=True, multiple=True),
        ],
        responses={201: PropertyMediaSerializer(many=True), 400: "Erro de validação"}
    )
    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        property_id = request.data.get('property')

        if not property_id:
            return Response({'error': 'O campo `property` é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

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

    @swagger_auto_schema(operation_summary="Get all Property-medias",)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Get Property-media by ID",)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update an existing Property-media",)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Detele a Property-media",)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
