from rest_framework import viewsets, filters, status
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from announcements.filters import AnnouncementFilter
from user_organizations.models import UserOrganization
from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementInputSerializer, AnnouncementIdInputSerializer, AnnouncementUpdateSerializer
from property.models import Property


class AnnouncementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Announcement.objects.select_related('property').all()
    serializer_class = AnnouncementSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnnouncementFilter
    ordering_fields = ['price', 'created_date']


    def get_permissions(self):
        if self.action == 'list':
            # Allow any user (even unauthenticated) to access list
            permission_classes = [AllowAny]
        else:
            # Require authentication for all other actions
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        user_org = UserOrganization.objects.filter(user=user).first()
        if not user_org:
            raise ValidationError("User has no associated organization.")

        property_instance = serializer.validated_data['property']
        if property_instance.organization != user_org.organization:
            raise ValidationError("Property does not belong to user's organization.")

        serializer.save(organization=user_org.organization)


    def get_serializer_class(self):
        if self.action == 'create':
            return AnnouncementInputSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return AnnouncementUpdateSerializer
        else:
            return AnnouncementSerializer


    @swagger_auto_schema(request_body=AnnouncementInputSerializer, operation_summary="Create a new Announcement")
    def create(self, request, *args, **kwargs):
        property_id = request.data.get("property_id") or request.data.get("property")
        organization_id = request.data.get("organization")

        try:
            property_instance = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise ValidationError("The selected property does not exist.")

        if organization_id is not None:
            if property_instance.organization.id != int(organization_id):
                raise ValidationError("The selected property does not belong to the given organization.")

        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
    request_body=AnnouncementUpdateSerializer,
    operation_summary="Update an existing Announcement"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get all Announcements",
        manual_parameters=[
            openapi.Parameter('district', openapi.IN_QUERY, description="Filter by district", type=openapi.TYPE_STRING),
            openapi.Parameter('municipality', openapi.IN_QUERY, description="Filter by municipality", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter(
            'is_active',
            openapi.IN_QUERY,
            description="Filter by active status",
            type=openapi.TYPE_BOOLEAN,
            enum=[True, False],
            default=True
        ),

            openapi.Parameter('typology', openapi.IN_QUERY, description="Filter by typology", type=openapi.TYPE_STRING),
            openapi.Parameter('num_wc', openapi.IN_QUERY, description="Filter by number of bathrooms", type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'property_type',
                openapi.IN_QUERY,
                description="Filter by property type",
                type=openapi.TYPE_STRING,
                enum=[choice[0] for choice in Property.TIPO_CHOICE]
            ),
            openapi.Parameter(
                'new_construction',
                openapi.IN_QUERY,
                description="Filter by new construction status",
                type=openapi.TYPE_STRING,
                enum=[choice[0] for choice in Property.NOVA_CONSTRUCAO_CHOICES]
            ),
            openapi.Parameter(
                'energy_certf',
                openapi.IN_QUERY,
                description="Filter by energy certificate",
                type=openapi.TYPE_STRING,
                enum=[choice[0] for choice in Property.CERTIFICADO_CHOICES]
            ),

            openapi.Parameter('gross_area', openapi.IN_QUERY, description="Filter by gross area", type=openapi.TYPE_NUMBER),
            openapi.Parameter('net_area', openapi.IN_QUERY, description="Filter by net area", type=openapi.TYPE_NUMBER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Get Announcement by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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

        organization_ids = UserOrganization.objects.filter(user=user).values_list('organization_id', flat=True)

        if not organization_ids:
            return Response({"detail": "User has no associated organizations."}, status=400)

        announcements = self.queryset.filter(property__organization_id__in=organization_ids)
        serializer = self.get_serializer(announcements, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get user's favourite Announcements",
        responses={200: AnnouncementSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='favourites', permission_classes=[IsAuthenticated])
    def favourites(self, request):
        user = request.user
        favourite_announcements = user.favourites.all()
        serializer = self.get_serializer(favourite_announcements, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Add an Announcement to user's favourites",
        request_body=AnnouncementIdInputSerializer
    )
    @action(detail=False, methods=['post'], url_path='add-favourite', permission_classes=[IsAuthenticated])
    def add_favourite(self, request):
        serializer = AnnouncementIdInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        announcement_id = serializer.validated_data['id']

        try:
            announcement = Announcement.objects.get(pk=announcement_id)
        except Announcement.DoesNotExist:
            return Response({"detail": "Announcement not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        user.favourites.add(announcement)
        return Response({"detail": "Added to favourites."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Remove an Announcement from user's favourites"
    )
    @action(detail=True, methods=['delete'], url_path='remove-favourite', permission_classes=[IsAuthenticated])
    def remove_favourite(self, request, pk=None):
        user = request.user
        try:
            announcement = Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            return Response({"detail": "Announcement not found."}, status=404)

        user.favourites.remove(announcement)
        return Response({"detail": "Removed from favourites."}, status=200)
