from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings 
from .models import Meeting, AgendaItem, Document, Annotation
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        # fields = ['id', 'agenda_item','file', 'uploaded_at']
        fields = '__all__'

class AgendaItemSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, required=False)

    class Meta:
        model = AgendaItem
        # fields = ['id', 'meeting', 'title', 'description', 'documents']
        fields = '__all__'

# class MeetingSerializer(serializers.ModelSerializer):
#     invitees = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
#     agenda_items = AgendaItemSerializer(many=True, required=False)

#     class Meta:
#         model = Meeting
#         fields = ['id', 'title', 'start_date', 'end_date', 'address', 'invitees', 'agenda_items']
#         # fields = '__all__'

#     def create(self, validated_data):
#         invitees_data = validated_data.pop('invitees', [])
#         agenda_items_data = validated_data.pop('agenda_items', [])
        
#         meeting = Meeting.objects.create(**validated_data)
        
#         for invitee in invitees_data:
#             meeting.invitees.add(invitee)
        
#         for agenda_item_data in agenda_items_data:
#             documents_data = agenda_item_data.pop('documents', [])
#             agenda_item = AgendaItem.objects.create(meeting=meeting, **agenda_item_data)
            
#             for document_data in documents_data:
#                 Document.objects.create(agenda_item=agenda_item, **document_data)
        
#         return meeting
    
class MeetingSerializer(serializers.ModelSerializer):
    invitees = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    agenda_items = AgendaItemSerializer(many=True, required=False)

    class Meta:
        model = Meeting
        fields = ['id', 'title', 'start_date', 'end_date', 'address', 'invitees', 'agenda_items']

    def create(self, validated_data):
        invitees_data = validated_data.pop('invitees', [])
        agenda_items_data = validated_data.pop('agenda_items', [])
        
        meeting = Meeting.objects.create(**validated_data)
        
        for invitee in invitees_data:
            meeting.invitees.add(invitee)
        
        for agenda_item_data in agenda_items_data:
            documents_data = agenda_item_data.pop('documents', [])
            agenda_item = AgendaItem.objects.create(meeting=meeting, **agenda_item_data)
            
            for document_data in documents_data:
                Document.objects.create(agenda_item=agenda_item, **document_data)

        # Send email notifications to invitees
        self.send_email_notifications(meeting, invitees_data)

        return meeting   


    def send_email_notifications(self, meeting, invitees):
        subject = f'New Meeting: {meeting.title}'
        message = (
            f'You have been invited to a new meeting.\n\n'
            f'Title: {meeting.title}\n'
            f'Start Date: {meeting.start_date}\n'
            f'End Date: {meeting.end_date}\n'
            f'Address: {meeting.address}\n\n'
            f'Please confirm your attendance.'
        )
        
        recipient_list = [invitee.email for invitee in invitees]
        
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            print("Email sent successfully to invitees.")
        except Exception as e:
            print(f"An error occurred while sending emails: {e}")


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['invitees'] = UserSerializer(instance.invitees.all(), many=True).data
        return representation
    
class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'