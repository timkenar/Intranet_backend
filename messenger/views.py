# In your messaging/views.py
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(sender=user) | self.queryset.filter(recipient=user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def users(self, request):
        users = User.objects.all()
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return Response(user_data)
