from django.db import models
from django.contrib.auth.models import User


# class Folder(models.Model):
#     name = models.CharField(max_length=255)
#     owner = models.ForeignKey(User, related_name='folders', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)


# class File(models.Model):
#     name = models.CharField(max_length=255)
#     folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)


# class Notification(models.Model):
#     message = models.TextField()
#     user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
