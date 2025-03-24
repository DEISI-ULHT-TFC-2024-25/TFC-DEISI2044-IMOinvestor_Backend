from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import Announcement
from .serializers import AnnouncementSerializer
from property.models import Property

class AnnouncementCreateView(generics.CreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def create(self, request, *args, **kwargs):
        # Ensure created_date and last_modified_date are set
        request.data["created_date"] = request.data.get("created_date", None)
        request.data["last_modified_date"] = request.data.get("last_modified_date", None)

        # Get property and organization from request data
        property_id = request.data.get("property")
        organization_id = request.data.get("organization")

        # Fetch the Property instance from the database
        try:
            property_instance = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise ValidationError("The selected property does not exist.")

        # Check if the organization from the property matches the given organization
        if property_instance.organization.id != int(organization_id):
            raise ValidationError(
                "The selected property does not belong to the given organization."
            )

        return super().create(request, *args, **kwargs)
