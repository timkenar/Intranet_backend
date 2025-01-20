from django.contrib.auth.models import User
from django.db import models
import os

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('folder', 'Folder'),
        ('file', 'File'),
    ]

    name = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    owner = models.ForeignKey(User, related_name='resources', on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_full_path(self):
        """
        Recursively construct the full path of the folder or file.
        """
        if self.parent:
            return os.path.join(self.parent.get_full_path(), self.name)
        return self.name
