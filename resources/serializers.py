from rest_framework import serializers
from .models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'resource_type', 'parent', 'owner', 'file', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']

class NestedFolderSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = ['id', 'name', 'resource_type', 'children']  # Add other fields if needed

    def get_children(self, obj):
        # Recursively fetch children folders
        if obj.resource_type == 'folder':  # Only fetch children for folders
            children = obj.children.filter(resource_type='folder')
            return NestedFolderSerializer(children, many=True).data
        return []

class CreateResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['name', 'resource_type', 'parent', 'file']

    def validate(self, data):
        if data['resource_type'] == 'folder' and data.get('file'):
            raise serializers.ValidationError("Folders cannot have files.")
        if data['resource_type'] == 'file' and not data.get('file'):
            raise serializers.ValidationError("Files must include an uploaded file.")
        return data