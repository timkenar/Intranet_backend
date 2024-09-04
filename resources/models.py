from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Folder(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not self.pk and user:
            self.created_by = user
        super().save(*args, **kwargs)

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not self.pk and user:
            self.created_by = user
        super().save(*args, **kwargs)

class Notification(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

# from django.db import models
# from django.contrib.auth.models import User

# class Folder(models.Model):
#     name = models.CharField(max_length=255)
#     created_by = models.ForeignKey(User, related_name='folders', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class File(models.Model):
#     name = models.CharField(max_length=255)
#     file = models.FileField(upload_to='uploads/', null=True, blank=True)
#     folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
#     created_by = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Notification(models.Model):
#     message = models.TextField()
#     user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# from django.db import models
# from django.contrib.auth.models import User

# class Folder(models.Model):
#     name = models.CharField(max_length=255)
#     owner = models.ForeignKey(User, related_name='folders', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class File(models.Model):
#     name = models.CharField(max_length=255)
#     fle = models.FileField(upload_to='uploads/', null=True, blank=True) 
#     folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Notification(models.Model):
#     message = models.TextField()
#     user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
