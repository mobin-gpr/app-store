from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
import threading

# Set up logging
logger = logging.getLogger(__name__)


class EmailThread(threading.Thread):
    def __init__(self, subject, to, context, template_name):
        self.subject = subject
        self.to = to
        self.context = context
        self.template_name = template_name
        super().__init__()

    def run(self):
        from_email = "no-reply@fox-web.ir"

        try:
            # Render the HTML message
            html_message = render_to_string(self.template_name, self.context)
            # Strip HTML tags for the plain text message
            plain_message = strip_tags(html_message)
            # Send the email
            send_mail(
                self.subject,
                plain_message,
                from_email,
                [self.to],
                html_message=html_message,
            )
        except Exception as e:
            # Log the exception
            logger.error(f"Failed to send email to {self.to}: {e}")


def send_styled_mail(subject, to, context, template_name):
    """
    Send an email with both HTML and plain text versions asynchronously.

    Parameters:
    - subject: Subject of the email.
    - to: Recipient's email address.
    - context: Context data for rendering the email template.
    - template_name: Name of the HTML template file.
    """
    email_thread = EmailThread(subject, to, context, template_name)
    email_thread.start()
