from nbformat import ValidationError
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from organization.models import Organization



from .models import Property
from .serializers import PropertySerializer
from .filters import PropertyFilter


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PropertyFilter
    ordering_fields = ['gross_area', 'net_area', 'min_price', 'max_price']


    def get_permissions(self):
        if self.action in ['create', 'update']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_summary="Get all Properties",
        manual_parameters=[
            openapi.Parameter('district', openapi.IN_QUERY, description="Filter by district", type=openapi.TYPE_STRING),
            openapi.Parameter('municipality', openapi.IN_QUERY, description="Filter by municipality", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
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
            openapi.Parameter('typology', openapi.IN_QUERY, description="Filter by typology", type=openapi.TYPE_STRING),
            openapi.Parameter('num_wc', openapi.IN_QUERY, description="Filter by number of bathrooms", type=openapi.TYPE_INTEGER),
            openapi.Parameter('gross_area', openapi.IN_QUERY, description="Filter by gross area", type=openapi.TYPE_NUMBER),
            openapi.Parameter('net_area', openapi.IN_QUERY, description="Filter by net area", type=openapi.TYPE_NUMBER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new Property")
    def create(self, request, *args, **kwargs):
        organization_ids = request.auth.get("organization_ids", []) if request.auth else []
        if not organization_ids:
            raise ValidationError("No organization associated with this user.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = Organization.objects.get(id=organization_ids[0])
        serializer.save(organization=organization)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @swagger_auto_schema(operation_summary="Get Property by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update an existing Property")
    def update(self, request, *args, **kwargs):
        organization_ids = request.auth.get("organization_ids", []) if request.auth else []
        if not organization_ids:
            raise ValidationError("No organization associated with this user.")
        
        mutable_data = request.data.copy()
        mutable_data['organization_id'] = organization_ids[0]
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=mutable_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Delete a Property")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    @action(detail=False, methods=["get"], url_path="with-announcement", permission_classes=[permissions.AllowAny])
    @swagger_auto_schema(operation_summary="Get Properties with an announcement")
    def with_announcement(self, request):
        properties = self.queryset.filter(announcement__isnull=False)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="without-announcement", permission_classes=[permissions.AllowAny])
    @swagger_auto_schema(operation_summary="Get Properties without an announcement")
    def without_announcement(self, request):
        properties = self.queryset.filter(announcement__isnull=True)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="my-organization",
        permission_classes=[IsAuthenticated]
    )
    @swagger_auto_schema(
        operation_summary="Get Properties by Authenticated User's Organization(s)",
        manual_parameters=[
            openapi.Parameter('district', openapi.IN_QUERY, description="Filter by district", type=openapi.TYPE_STRING),
            openapi.Parameter('municipality', openapi.IN_QUERY, description="Filter by municipality", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
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
            openapi.Parameter('typology', openapi.IN_QUERY, description="Filter by typology", type=openapi.TYPE_STRING),
            openapi.Parameter('num_wc', openapi.IN_QUERY, description="Filter by number of bathrooms", type=openapi.TYPE_INTEGER),
            openapi.Parameter('gross_area', openapi.IN_QUERY, description="Filter by gross area", type=openapi.TYPE_NUMBER),
            openapi.Parameter('net_area', openapi.IN_QUERY, description="Filter by net area", type=openapi.TYPE_NUMBER),
        ]
    )
    def my_organization(self, request):
        organization_ids = request.auth.get("organization_ids", []) if request.auth else []
    
        if not organization_ids:
            return Response({"detail": "No organization associated with this user."}, status=403)
    
        base_queryset = self.queryset.filter(organization_id__in=organization_ids)
    
        filtered_queryset = PropertyFilter(request.GET, queryset=base_queryset).qs
    
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
    
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)