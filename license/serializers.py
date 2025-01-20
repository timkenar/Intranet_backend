# license/serializers.py

from rest_framework import serializers
from .models import Subscription
# License

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'name', 'duration', 'features', 'max_users']

# class LicenseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = License
#         fields = ['id', 'user', 'subscription', 'start_date', 'end_date', 'is_active']
