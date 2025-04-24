from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Municipality
from .serializers import MunicipalitySerializer, DistrictInputSerializer
from drf_yasg.utils import swagger_auto_schema

class MunicipalitiesByDistrictView(APIView):

    @swagger_auto_schema(
        request_body=DistrictInputSerializer,
        responses={200: MunicipalitySerializer(many=True)},
        operation_description="Get municipalities by district ID (sent in POST body)"
    )
    def post(self, request):
        serializer = DistrictInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        district_id = serializer.validated_data['district_id']
        
        municipalities = Municipality.objects.filter(district_id=district_id)
        response_serializer = MunicipalitySerializer(municipalities, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
