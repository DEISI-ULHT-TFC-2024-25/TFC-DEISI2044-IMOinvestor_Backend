import secrets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from subscriptions.models import Subscription
from datetime import timedelta

class UpdateSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user  # Get the currently authenticated user

        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(days=30)

        subscription, created = Subscription.objects.update_or_create(
            user=user,
            defaults={
                "token": token,
                "expires_at": expires_at,
            }
        )

        return Response({
            "message": "Subscription updated" if not created else "Subscription created",
            "user_id": user.id,
            "token": subscription.token,
            "expires_at": subscription.expires_at,
        }, status=status.HTTP_200_OK)
