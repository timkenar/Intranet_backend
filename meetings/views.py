from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
from .models import Meeting, AgendaItem, Document
from .serializers import MeetingSerializer, AgendaItemSerializer, DocumentSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.conf import settings
from .models import Meeting
from .utils import merge_meeting_documents
import os

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    # permission_classes = [IsAuthenticated]

class AgendaItemViewSet(viewsets.ModelViewSet):
    queryset = AgendaItem.objects.all()
    serializer_class = AgendaItemSerializer
    # permission_classes = [IsAuthenticated]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes = [IsAuthenticated]



@api_view(['GET'])
def generate_boardpack(request, meeting_id):
    try:
        meeting = Meeting.objects.get(pk=meeting_id)
        boardpack_path = merge_meeting_documents(meeting)
        print('Boarpack Path is', boardpack_path)

        # Serve the merged PDF file
        with open(boardpack_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline;filename={os.path.basename(boardpack_path)}'
            return response
    except Meeting.DoesNotExist:
        return Response({"error": "Meeting not found"}, status=404)