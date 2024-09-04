from rest_framework import serializers
from .models import Folder, File, Notification


class FileSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')  # Use the username or other relevant field
    folder = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all())  # Ensure this is set up as needed
    
    
    class Meta:
        model = File
        fields = ('id', 'name', 'file', 'folder', 'created_by', 'created_at')

class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True) 

    created_by = serializers.ReadOnlyField(source='created_by.username')  # Use the username or other relevant field
    
    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_by', 'created_at')


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Use the username or other relevant field
    
    class Meta:
        model = Notification
        fields = ('id', 'message', 'user', 'created_at')
