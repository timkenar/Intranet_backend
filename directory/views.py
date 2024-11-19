from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.conf import settings

from .utils import send_invitation_email  # Updated to use the utility function
from .serializers import UserInvitationSerializer, UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class CurrentUserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data) 
    
#Inviting New Users to the system 

# New code for user invitation;

import random
import string

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class UserInvitationView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = UserInvitationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            role = data['role']

            # Generate a temporary password
            temp_password = generate_random_password() # Built-in method for random passwords

            # Create the user with the temporary password
            user = User.objects.create_user(
                username=email,
                email=email,
                password=temp_password,
                first_name=first_name,
                last_name=last_name
            )
            user.groups.add(role)  # Assuming roles are handled via groups
            user.is_active = False  # User needs to complete signup
            user.save()

            # Construct the invitation link
            invitation_link = f"{settings.FRONTEND_URL}/invite?email={email}"

            # Use the utility function to send the email
            send_invitation_email(first_name, last_name, email, invitation_link, temp_password)

            return Response({'message': 'Invitation sent successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserInvitationView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request):
#         serializer = UserInvitationSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.save()
#             first_name = data['first_name']
#             last_name = data['last_name']
#             email = data['email']
#             role = data['role']

#             # Generate an invitation link (customize the URL as needed)
#             invitation_link = f"{settings.FRONTEND_URL}/invite?email={email}&role={role.id}"
            
#             # Send email invitation
#             send_mail(
#                 'You are invited to join the system',
#                 f'Hi {first_name} {last_name},\n\n'
#                 f'You have been invited to join our Boardmeets system. '
#                 f'Please click the following link to create your account: {invitation_link}',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [email],
#                 fail_silently=False,
#             )

#             return Response({'message': 'Invitation sent successfully.'}, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)