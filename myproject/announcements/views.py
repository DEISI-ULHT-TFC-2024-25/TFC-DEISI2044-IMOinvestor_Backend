from django.shortcuts import render
from rest_framework import generics
from .models import Announcement
from .serializers import AnnouncementSerializer

class AnnouncementCreateView(generics.CreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def create(self, request, *args, **kwargs):
        request.data["created_date"] = request.data.get("created_date", None)
        request.data["last_modified_date"] = request.data.get("last_modified_date", None)
        return super().create(request, *args, **kwargs)


