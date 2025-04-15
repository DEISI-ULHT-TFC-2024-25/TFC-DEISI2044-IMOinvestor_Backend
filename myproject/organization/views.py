from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from .serializers import OrganizationSerializer

class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def create(self, request, *args, **kwargs):
        request.data["created_date"] = request.data.get("created_date", None)
        request.data["last_modified_date"] = request.data.get("last_modified_date", None)
        return super().create(request, *args, **kwargs)

class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = []  # Acesso público