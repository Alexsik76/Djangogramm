from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def create_inactive_user(form):
    user = form.save(commit=False)
    user.is_active = False
    user.set_unusable_password()
    user.username = user.email
    return user


def create_mesage_body(user, request):
    message_body = render_to_string('registration/activation_email.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    return message_body
