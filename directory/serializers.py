from rest_framework import serializers
from django.contrib.auth.models import User,Group

from .models import UserRole, Role

class UserRoleSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')
     
    class Meta:
        model = UserRole
        fields = ['role']
 

class UserSerializer(serializers.ModelSerializer):
    
    roles = UserRoleSerializer(many=True, read_only=True, source='user_roles')
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'roles' , 'group']


from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


# Invitation Serializer
class UserInvitationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    def create(self, validated_data):
        return validated_data  # Return all validated data for email processing
    
    
    