import logging

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings

from accounts.mail_sender import send_html
from accounts.token_creator import TokenGenerator
from smartcontract import celery_app


@celery_app.task
def send_confirmation_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        generator = TokenGenerator()
        email = user.email
        message = render_to_string('accounts/email/activate_letter.html', {
            'user': user,
            'domain': settings.APP_DOMAIN,  # change to get_current_site(request)
            'uid': urlsafe_base64_encode(force_bytes(user_id)),
            'token': generator.make_token(user),
        })
        send_html("Smart Contract email verification", message, settings.DEFAULT_FROM_EMAIL, email)
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
