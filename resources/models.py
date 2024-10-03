from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
