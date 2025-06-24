from rest_framework import viewsets, permissions
from .models import Investment
from .serializers import InvestmentSerializer
from rest_framework.exceptions import PermissionDenied

class InvestmentViewSet(viewsets.ModelViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Investment.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return Investment.objects.none()

        return Investment.objects.filter(user=user)


    def perform_create(self, serializer):
        # Set the user to the authenticated user on create
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Allow update only if the investment belongs to the user
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You cannot modify another user's investment.")
        serializer.save()

    def perform_destroy(self, instance):
        # Allow delete only if the investment belongs to the user
        if instance.user != self.request.user:
            raise PermissionDenied("You cannot delete another user's investment.")
        instance.delete()
