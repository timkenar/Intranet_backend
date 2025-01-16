import secrets
import string
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.core.mail import send_mail
from .serializers import UserInvitationSerializer, UserSerializer, GroupSerializer
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from directory.models import UserInvitation




class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class CurrentUserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data) 
    
#Added the group feature    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated] 
    
    
class UserInvitationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def generate_random_password(self):
        """Generates a random, secure password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for i in range(12))  # 12-character password

    def create(self, request):
        serializer = UserInvitationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            role = data['role']

            # Generate a random temporary password
            temporary_password = self.generate_random_password()

            # Create the user instance and set the temporary password
            user = User.objects.create_user(
                username=email,  # Using the email as the username
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=temporary_password,
            )
            user.is_active = False  # Ensure user is inactive until they reset their password
            user.save()

            # Generate the password reset link
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())  # No need to decode here
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"  # Custom reset link

            # Create the invitation in the database
            invitation = UserInvitation.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role,
                invited_by=request.user,  # The admin who invited the user
                token=token,  # Store the token for future reference
            )

            # Now send the invitation email
            email_subject = 'You are invited to join the system'
            email_body = render_to_string(
                'invitation_email.html',  # Path to the email template
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role.name,  # Assuming role has a 'name' attribute
                    'reset_link': reset_link,  # Pass the reset password link
                    'temporary_password': temporary_password,  # Add the temporary password here
                }
            )

            # Send email (both plain-text and HTML version)
            send_mail(
                subject=email_subject,
                message="",  # Plain text body, in case HTML is not supported by the client
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=email_body,  # HTML message is key here
                fail_silently=False,
            )

            return Response({'message': 'Invitation sent successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Reset Password Code
class ResetPasswordViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny] 

    def reset_password(self, request, uidb64, token):
        try:
            # Decode the uid and get the user object
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": _("Invalid reset link.")}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the reset token is valid
        if not default_token_generator.check_token(user, token):
            return Response({"detail": _("Invalid or expired token.")}, status=status.HTTP_400_BAD_REQUEST)

        # Get the new password from the request data
        new_password = request.data.get("new_password")
        if not new_password:
            return Response({"detail": _("New password is required.")}, status=status.HTTP_400_BAD_REQUEST)

        # Reset the user's password
        user.set_password(new_password)
        user.is_active = True  # Activate the user after password reset
        user.save()

        # Optionally, keep the user logged in after resetting the password
        update_session_auth_hash(request, user)

        return Response({"detail": _("Password has been reset successfully.")}, status=status.HTTP_200_OK)
