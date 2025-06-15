from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Property
from .serializers import PropertySerializer
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]  # Adjust as needed
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PropertyFilter
    ordering_fields = ['area_bruta', 'area_util', 'preco_minimo', 'preco_maximo']

    @swagger_auto_schema(
        operation_summary="Get all Properties",
        manual_parameters=[
            openapi.Parameter('district', openapi.IN_QUERY, description="Filtrar por distrito", type=openapi.TYPE_STRING),
            openapi.Parameter('municipality', openapi.IN_QUERY, description="Filtrar por município", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Preço mínimo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Preço máximo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('property_type', openapi.IN_QUERY, description="Filtrar por tipo de imóvel", type=openapi.TYPE_STRING),
            openapi.Parameter('nova_construcao', openapi.IN_QUERY, description="Filtrar por nova construção", type=openapi.TYPE_STRING),
            openapi.Parameter('preco_minimo', openapi.IN_QUERY, description="Filtrar por preço mínimo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('preco_maximo', openapi.IN_QUERY, description="Filtrar por preço máximo", type=openapi.TYPE_NUMBER),


            openapi.Parameter('tipologia', openapi.IN_QUERY, description="Filtrar por tipologia", type=openapi.TYPE_STRING),
            openapi.Parameter('numero_casas_banho', openapi.IN_QUERY, description="Filtrar por número de casas de banho", type=openapi.TYPE_INTEGER),
            openapi.Parameter('certificado_energetico', openapi.IN_QUERY, description="Filtrar por certificado energético", type=openapi.TYPE_STRING),

            openapi.Parameter('area_bruta', openapi.IN_QUERY, description="Filtrar por área bruta", type=openapi.TYPE_NUMBER),
            openapi.Parameter('area_util', openapi.IN_QUERY, description="Filtrar por área útil", type=openapi.TYPE_NUMBER),
    

        ]
    )
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
    @swagger_auto_schema(
        operation_summary="Get Properties by Authenticated User's Organization(s)",
        manual_parameters=[
            openapi.Parameter('district', openapi.IN_QUERY, description="Filtrar por distrito", type=openapi.TYPE_STRING),
            openapi.Parameter('municipality', openapi.IN_QUERY, description="Filtrar por município", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Preço mínimo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Preço máximo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('property_type', openapi.IN_QUERY, description="Filtrar por tipo de imóvel", type=openapi.TYPE_STRING),
            openapi.Parameter('nova_construcao', openapi.IN_QUERY, description="Filtrar por nova construção", type=openapi.TYPE_STRING),
            openapi.Parameter('preco_minimo', openapi.IN_QUERY, description="Filtrar por preço mínimo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('preco_maximo', openapi.IN_QUERY, description="Filtrar por preço máximo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('tipologia', openapi.IN_QUERY, description="Filtrar por tipologia", type=openapi.TYPE_STRING),
            openapi.Parameter('numero_casas_banho', openapi.IN_QUERY, description="Filtrar por número de casas de banho", type=openapi.TYPE_INTEGER),
            openapi.Parameter('certificado_energetico', openapi.IN_QUERY, description="Filtrar por certificado energético", type=openapi.TYPE_STRING),
            openapi.Parameter('area_bruta', openapi.IN_QUERY, description="Filtrar por área bruta", type=openapi.TYPE_NUMBER),
            openapi.Parameter('area_util', openapi.IN_QUERY, description="Filtrar por área útil", type=openapi.TYPE_NUMBER),
        ]
    )
    def by_organization(self, request):
        organization_ids = request.auth.get("organization_ids", []) if request.auth else []
    
        if not organization_ids:
            return Response({"detail": "No organization associated with this user."}, status=403)
    
        # Filter properties by organization
        base_queryset = self.queryset.filter(organization_id__in=organization_ids)
    
        # Apply filters using PropertyFilter
        filtered_queryset = PropertyFilter(request.GET, queryset=base_queryset).qs
    
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
    
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
