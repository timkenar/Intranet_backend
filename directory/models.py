from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Role(models.Model):
    ADMIN = 'admin'
    CREATOR = 'creator'
    MEMBER = 'member'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CREATOR, 'Creator'),
        (MEMBER, 'Member'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    
    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'role')
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"



class History(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()


class UserInvitation(models.Model):
    email = models.EmailField(unique=True)  # Email for the invited user
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Admin who sent the invite
    is_active = models.BooleanField(default=True)  # Whether the invitation is active or used
    token = models.CharField(max_length=255, null=True, blank=True)  # Optional token for tracking reset requests
    sent_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the invitation is sent
    used_at = models.DateTimeField(null=True, blank=True)  # Timestamp when the invitation was used

    def __str__(self):
        return f"Invitation for {self.first_name} {self.last_name} ({self.email})"
