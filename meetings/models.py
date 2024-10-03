from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    address = models.TextField()
    invitees = models.ManyToManyField(User, related_name='meetings')
    published = models.BooleanField

    def __str__(self):
        return self.title

class AgendaItem(models.Model):
    meeting = models.ForeignKey(Meeting, related_name='agenda_items', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.meeting.title} - {self.title}"

class Document(models.Model):
    agenda_item = models.ForeignKey(AgendaItem, related_name='documents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='meeting_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.agenda_item}"
    
class Annotation(models.Model):
    ANNOTATION_TYPES = [
        ('highlight', 'Highlight'),
        ('text', 'Text'),
        ('freehand', 'Freehand'),
        ('comment', 'Comment'),
        ('underline', 'Underline'),
    ]
    
    document = models.ForeignKey(Document, related_name='annotations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='annotations', on_delete=models.CASCADE)
    annotation_type = models.CharField(max_length=20, choices=ANNOTATION_TYPES)
    coordinates = models.JSONField()  # Stores coordinates for highlights, freehand, and underline
    text = models.TextField(blank=True, null=True)  # Stores the comment note or text if applicable
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.annotation_type.capitalize()} by {self.user.username} on {self.document}"