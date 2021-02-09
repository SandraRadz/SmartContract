from django.core.mail import send_mail


def send_plain_text(title, message, email_from, email_to):
    send_mail(title, message, email_from, [email_to],
              fail_silently=False)


def send_html(title, message, email_from, email_to):
    send_mail(title, message, email_from, [email_to],
              fail_silently=False, html_message=message)
