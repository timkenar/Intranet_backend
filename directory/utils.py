from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_invitation_email(first_name, last_name, email, invitation_link, temp_password):
    """
    Sends an invitation email to the specified email address using an HTML template.
    """
    subject = 'You are invited to join Boardmeets'
    from_email = settings.DEFAULT_FROM_EMAIL

    # Render the HTML template
    html_content = render_to_string('emails/invitation_email.html', {
        'first_name': first_name,
        'last_name': last_name,
        'invitation_link': invitation_link,
        'temp_password': temp_password,
    })

    # Send the email
    email_message = EmailMessage(subject, html_content, from_email, [email])
    email_message.content_subtype = 'html'  # Mark as HTML content
    email_message.send(fail_silently=False)
