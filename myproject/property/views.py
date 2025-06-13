from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Property
from .serializers import PropertySerializer
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]  # Adjust as needed

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

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    @action(detail=False, methods=["get"], url_path="with-announcement", permission_classes=[permissions.AllowAny])
    @swagger_auto_schema(operation_summary="Properties with an announcement")
    def with_announcement(self, request):
        properties = self.queryset.filter(announcement__isnull=False)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="without-announcement", permission_classes=[permissions.AllowAny])
    @swagger_auto_schema(operation_summary="Properties without an announcement")
    def without_announcement(self, request):
        properties = self.queryset.filter(announcement__isnull=True)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="my-organization", permission_classes=[IsAuthenticated])
    @swagger_auto_schema(operation_summary="Get Properties by Authenticated User's Organization(s)")
    def by_organization(self, request):
        organization_ids = request.auth.get("organization_ids", []) if request.auth else []

        if not organization_ids:
            return Response({"detail": "No organization associated with this user."}, status=403)

        properties = self.queryset.filter(organization_id__in=organization_ids)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)
