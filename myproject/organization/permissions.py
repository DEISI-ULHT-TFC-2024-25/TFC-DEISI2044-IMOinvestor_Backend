import jwt
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.conf import settings

class IsTokenOrganization(permissions.BasePermission):
    """
    Manually decodes JWT to check if the token has required organization_ids.
    """

    def has_permission(self, request, view):
        # Get organization ID from URL
        try:
            org_id = int(view.kwargs.get('id'))
        except (TypeError, ValueError):
            raise PermissionDenied(detail="Invalid or missing organization ID in URL.")

        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise PermissionDenied(detail="Authorization header missing or invalid.")

        token = auth_header.split(' ')[1]

        try:
            # Decode token manually using your secret key
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise PermissionDenied(detail="Token has expired.")
        except jwt.InvalidTokenError:
            raise PermissionDenied(detail="Invalid token.")

        org_ids = decoded.get("organization_ids")

        if not org_ids:
            raise PermissionDenied(detail="Token missing 'organization_ids'.")

        if org_id not in org_ids:
            raise PermissionDenied(detail="You do not have permission for this organization.")

        return True
