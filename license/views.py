from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Subscription
# License
from .serializers import SubscriptionSerializer
# LicenseSerializer
from django.utils import timezone
from datetime import timedelta

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

# class LicenseViewSet(viewsets.ModelViewSet):
#     queryset = License.objects.all()
#     serializer_class = LicenseSerializer

#     def create(self, request, *args, **kwargs):
#         subscription_id = request.data.get('subscription_id')
#         subscription = Subscription.objects.get(id=subscription_id)
        
#         current_user_count = License.objects.filter(subscription=subscription, is_active=True).count()
#         if current_user_count >= subscription.max_users:
#             return Response(
#                 {"detail": "User limit reached for this subscription plan."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         license = License.objects.create(
#             user=request.user,
#             subscription=subscription,
#             end_date=timezone.now() + timedelta(days=subscription.duration)
#         )
#         serializer = self.get_serializer(license)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
