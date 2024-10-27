# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from django.contrib.auth.models import User
# import pywhatkit as kit

# @receiver(post_save, sender=Message)
# def send_whatsapp_notification(sender, instance, created, **kwargs):
#     if created:
#         recipient = instance.recipient
#         sender = instance.sender
#         message_url = "https://yourapp.com/messenger"  # URL to view the message

#         # Construct the WhatsApp notification message
#         whatsapp_message = f"You have a new message from {sender.username}. Open your messenger to view: {message_url}"

#         # Retrieve the recipient's phone number from their profile
#         phone_number = recipient.profile.phone_number
#         if phone_number:  # Ensure the phone number exists
#             try:
#                 # Send the WhatsApp message instantly
#                 kit.sendwhatmsg_instantly(phone_number, whatsapp_message)
#             except Exception as e:
#                 print(f"Failed to send WhatsApp message: {e}")
