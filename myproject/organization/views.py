from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from .models import Organization
from .serializers import OrganizationSerializer
from .permissions import IsTokenOrganization
from django.conf import settings
import jwt


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTokenOrganization()]
        return []

    def get_object(self):
        # Para update, validando organização a partir do token
        obj = super().get_object()
        if self.action in ['update', 'partial_update', 'destroy']:
            auth_header = self.request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                raise PermissionDenied("Authorization header is missing or invalid.")

            token = auth_header.split(' ')[1]

            try:
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                raise PermissionDenied("Token has expired.")
            except jwt.InvalidTokenError:
                raise PermissionDenied("Invalid token.")

            organization_ids = decoded.get("organization_ids")
            if not organization_ids or str(obj.id) not in map(str, organization_ids):
                raise PermissionDenied("You can only modify your own organization.")

        return obj

    @swagger_auto_schema(operation_summary="Listar organizações")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Criar organização")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Detalhar organização")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Atualizar organização")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Excluir organização")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
