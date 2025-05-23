from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import MethodNotAllowed

from .models import Municipality
from .serializers import MunicipalitySerializer, DistrictInputSerializer


class MunicipalityViewSet(viewsets.ModelViewSet):

    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Listar municípios")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Criar município")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Obter município por ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Atualizar município")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Deletar município")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    @swagger_auto_schema(
        method='post',
        request_body=DistrictInputSerializer,
        responses={200: MunicipalitySerializer(many=True)},
        operation_summary="Buscar municípios por ID do distrito"
    )
    @action(detail=False, methods=["post"], url_path="by-district")
    def by_district(self, request):
        serializer = DistrictInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        district_id = serializer.validated_data["district_id"]
        municipalities = Municipality.objects.filter(district_id=district_id)
        response_serializer = self.get_serializer(municipalities, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
