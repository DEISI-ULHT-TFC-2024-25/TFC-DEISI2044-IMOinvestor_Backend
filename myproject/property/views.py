from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions 
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated


from .models import Property
from .serializers import PropertySerializer

class PropertyCreateView(APIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


    @swagger_auto_schema(request_body=PropertySerializer,
                         operation_summary="Criar uma nova propriedade",)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            property_instance = serializer.save()  # Saves and returns the instance
            return Response(self.serializer_class(property_instance).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    


class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'id'


class PropertyDeleteView(generics.DestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class PropertyUpdateView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class PropertyByOrganizationView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        organization_id = self.kwargs.get('organization_id')
        return Property.objects.filter(organization_id=organization_id)
