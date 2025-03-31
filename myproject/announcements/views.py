from django.shortcuts import render
from rest_framework import generics,filters,viewsets
from rest_framework.exceptions import ValidationError
from .models import Announcement
from .serializers import AnnouncementSerializer
from property.models import Property
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AnnouncementFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class AnnouncementCreateView(generics.CreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def create(self, request, *args, **kwargs):
        # Ensure created_date and last_modified_date are set
        request.data["created_date"] = request.data.get("created_date", None)
        request.data["last_modified_date"] = request.data.get("last_modified_date", None)

        # Get property and organization from request data
        property_id = request.data.get("property")
        organization_id = request.data.get("organization")

        # Fetch the Property instance from the database
        try:
            property_instance = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise ValidationError("The selected property does not exist.")

        # Check if the organization from the property matches the given organization
        if property_instance.organization.id != int(organization_id):
            raise ValidationError(
                "The selected property does not belong to the given organization."
            )

        return super().create(request, *args, **kwargs)



class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.select_related('property').all()
    serializer_class = AnnouncementSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnnouncementFilter
    ordering_fields = ['price', 'created_date']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('district', openapi.IN_QUERY, description="Filter by district", type=openapi.TYPE_STRING),
            openapi.Parameter('municipality', openapi.IN_QUERY, description="Filter by municipality", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Filter by minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Filter by maximum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('property_type', openapi.IN_QUERY, description="Filter by property type", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)