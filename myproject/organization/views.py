from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from .serializers import OrganizationSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTokenOrganization
from django.conf import settings
import jwt



from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsTokenOrganization(BasePermission):
    """
    Allows access only if the organization ID in the token matches the target org ID in the URL.
    """

    def has_permission(self, request, view):
        # Safe method check is optional, based on your needs
        return True  # We handle the check in `has_object_permission`

    def has_object_permission(self, request, view, obj):
        # Extract org ID from token (assumes it's in the token payload)
        token_org_id = request.auth.get('organization_id')

        if token_org_id is None:
            raise PermissionDenied("Token missing organization_id")

        if str(obj.id) != str(token_org_id):
            raise PermissionDenied("You can only update/delete your own organization")

        return True




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
    permission_classes = []  

class OrganizationDetailView(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = 'id'


class OrganizationDeleteView(generics.DestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsTokenOrganization]
    lookup_field = 'id'


class OrganizationUpdateView(generics.UpdateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Extract token from the header
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
        if not organization_ids:
            raise PermissionDenied("No organization ID found in token.")

        # You can adjust this if your logic allows multiple orgs
        org_id = organization_ids[0]

        try:
            return Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            raise PermissionDenied("Organization not found or access denied.")
