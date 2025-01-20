# license/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('essential', 'Essential'),
        ('premium', 'Premium'),
        ('ultimate', 'Ultimate'),
    ]

    APPLICATIONS = [
        'intranet',
        'messenger',
        'resources',
        'meetings',
    ]

    name = models.CharField(max_length=255, choices=PLAN_CHOICES)
    duration = models.PositiveIntegerField()  # Duration in days
    features = models.JSONField(default=list)  # Store feature flags as a list
    max_users = models.PositiveIntegerField()  # Max active users for this plan
    allowed_apps = models.JSONField(default=list)

    def __str__(self):
        return self.name


# class UserGroup(models.Model): 
#     name = models.CharField(max_length=255)
#     users = models.ManyToManyField(User, related_name='user_groups')

#     def __str__(self):
#         return self.name


# class License(models.Model):
#     group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True, blank=True)  # Allow for group assignments
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional direct user assignment
#     subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField()
#     is_active = models.BooleanField(default=True)

#     def is_valid(self):
#         return self.is_active and self.end_date > timezone.now()

#     def __str__(self):
#         if self.user:
#             return f"{self.user.username} - {self.subscription.name} License"
#         elif self.group:
#             return f"{self.group.name} - {self.subscription.name} License"
#         return f"Unassigned License - {self.subscription.name}"