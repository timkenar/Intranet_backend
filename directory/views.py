from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

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
    
    # Email Template
    
    
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserInvitationSerializer

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

            # Generate the invitation link (customize as needed)
            invitation_link = f"{settings.FRONTEND_URL}/invite?email={email}&role={role.id}"

            # Render the email content using the template
            email_subject = 'You are invited to join the system'
            email_body = render_to_string(
                'invitation_email.html',  # Path to the email template
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role.name,  # Assuming role has a 'name' attribute
                    'invitation_link': invitation_link,
                }
            )

            # Send the email
            send_mail(
                subject=email_subject,
                message='',# HTML email body
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=email_body,
                fail_silently=False,
            )

            return Response({'message': 'Invitation sent successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
