from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Announcement
from .serializers import AnnouncementSerializer
from .filters import AnnouncementFilter
from property.models import Property


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related('property').all()
    serializer_class = AnnouncementSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnnouncementFilter
    ordering_fields = ['price', 'created_date']

    @swagger_auto_schema(operation_summary="Create a new Announcement")
    def create(self, request, *args, **kwargs):
        property_id = request.data.get("property")
        organization_id = request.data.get("organization")

        try:
            property_instance = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise ValidationError("The selected property does not exist.")

        if property_instance.organization.id != int(organization_id):
            raise ValidationError("The selected property does not belong to the given organization.")

        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get all Announcements",
        manual_parameters=[
            openapi.Parameter('district', openapi.IN_QUERY, description="Filtrar por distrito", type=openapi.TYPE_STRING),
            openapi.Parameter('municipality', openapi.IN_QUERY, description="Filtrar por município", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Preço mínimo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Preço máximo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('property_type', openapi.IN_QUERY, description="Filtrar por tipo de imóvel", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Get Announcement by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update an existing Announcement")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete an Announcement")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    @swagger_auto_schema(operation_summary="Get Announcements by Organization")
    @action(detail=False, methods=['get'], url_path='my-organization', permission_classes=[IsAuthenticated])
    def my_organization_announcements(self, request):
        user = request.user
        organizations = user.institution.all()

        if not organizations.exists():
            return Response({"detail": "User has no associated organizations."}, status=400)

        announcements = self.queryset.filter(property__organization__in=organizations)
        serializer = self.get_serializer(announcements, many=True)
        return Response(serializer.data)
