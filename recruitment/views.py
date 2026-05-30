from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import threading
from django.template.loader import render_to_string


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, from_email, recipient_list):
        self.subject = subject
        self.html_content = html_content
        self.from_email = from_email
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            subject=self.subject,
            body=self.html_content,
            from_email=self.from_email,
            to=self.recipient_list,
        )
        msg.attach_alternative(self.html_content, "text/html")
        msg.send(fail_silently=False)


def send_email_job(request, recipient_list, data):
    subject = "Une nouvelle candidature a été reçue avec succès"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = recipient_list
    print("recipient_list----------------------->\n \n ",recipient_list)
    html_content = render_to_string('snippets/email_job.html',  {'data': data})
    # Start the thread
    EmailThread(subject, html_content, from_email, recipient_list).start()
    print("Email sent ✅")




def send_email_contact(request, recipient_list, data):
    subject = "Un nouveau contact a été reçue avec succès"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = recipient_list
    print("recipient_list----------------------->\n \n ",recipient_list)
    html_content = render_to_string('snippets/email_contact.html',  {'data': data})
    # Start the thread
    EmailThread(subject, html_content, from_email, recipient_list).start()
    print("Email sent ✅")
