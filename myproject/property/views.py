from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Property
from .serializers import PropertySerializer
from rest_framework.exceptions import MethodNotAllowed


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Get all Properties")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new Property")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Get Property by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update an existing Property")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a Property")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="organization/(?P<organization_id>[^/.]+)",
            permission_classes=[permissions.AllowAny])
    def by_organization(self, request, organization_id=None):
        properties = self.queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
    
    @action(detail=False, methods=["get"], url_path="with-announcement", permission_classes=[permissions.AllowAny])
    @swagger_auto_schema(operation_summary="Properties with an announcement",)
    def with_announcement(self, request):
        properties = self.queryset.filter(announcement__isnull=False)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="without-announcement",
            permission_classes=[permissions.AllowAny])
    @swagger_auto_schema(operation_summary="Properties without an announcement",)
    def without_announcement(self, request):
        properties = self.queryset.filter(announcement__isnull=True)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)

    
    
