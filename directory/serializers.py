from rest_framework import serializers
from django.contrib.auth.models import Group, User

from .models import UserRole, Role, Group, UserGroup

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

#For group serializers
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'description']


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['user', 'group', 'role']

    def validate(self, data):
        user = data.get('user')
        role = data.get('role')

        # Default to the user's system-level role if no role is provided
        if not role:
            system_role = user.system_role.role  # Retrieve the user's global/system role
            data['role'] = system_role

        return data

# Invitation Serializer
class UserInvitationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    def create(self, validated_data):
        return validated_data  # Return all validated data for email processing
    
    
    