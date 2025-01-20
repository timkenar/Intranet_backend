# license/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet
# LicenseViewSet

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)
# router.register(r'licenses', LicenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
