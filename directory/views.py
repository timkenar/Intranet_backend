from rest_framework import generics
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .serializers import UserInvitationSerializer

from .serializers import UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    

    
#Inviting New Users to the system 

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

            # Generate an invitation link (customize the URL as needed)
            invitation_link = f"{settings.FRONTEND_URL}/invite?email={email}&role={role.id}"
            
            # Send email invitation
            send_mail(
                'You are invited to join the system',
                f'Hi {first_name} {last_name},\n\n'
                f'You have been invited to join our Boardmeets system. '
                f'Please click the following link to create your account: {invitation_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return Response({'message': 'Invitation sent successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)