import datetime
import logging
import time
from urllib.parse import quote
import uuid

import requests
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.urls import reverse
from django.views import View

from accounts.token_creator import TokenGenerator
from .models import User
from .forms import EditUserForm, UserRegistrationForm, UserAuthForm, UserPasswordSetupForm
from .tasks import send_confirmation_email


@login_required
def personal_information(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'accounts/personal_information.html', context)


@login_required
def edit_personal_information(request):
    user = request.user
    email = user.email
    if request.method == 'POST':
        form = EditUserForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            if email == user.email:
                messages.success(request, "Information were successfully updated")
            else:
                # send_confirmation_email.delay(user.id)
                send_confirmation_email(user.id)
                messages.warning(request, "Information were successfully updated. Please confirm your email address "
                                          "to complete your registration. It's easy "
                                          "- just check your email and click on the confirmation link.")
            return redirect(reverse('personal_information'))
    else:
        form = EditUserForm(instance=user)
    context = {
        'form': form
    }
    return render(request, 'accounts/edit_personal_information.html', context)


def login_view(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    do_redirect = False

    if request.user.is_authenticated:
        if redirect_to == request.path:
            raise ValueError('Redirection loop for authenticated user detected.')
        return redirect(reverse('homepage'))
    elif request.method == 'POST':
        login_form = UserAuthForm(request, data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            return redirect(reverse('homepage'))
    else:
        login_form = UserAuthForm(request)
    register_form = UserRegistrationForm()
    context = {
        'register_form': register_form,
        'login_form': login_form
    }
    return render(request, 'accounts/login.html', context)


def register(request):
    from .forms import UserRegistrationForm
    if request.user.is_authenticated:
        return redirect(reverse('homepage'))

    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            # send_confirmation_email.delay(user.id)
            send_confirmation_email(user.id)
            messages.warning(request, "Thanks for joining Smart Contract! Please confirm your email address to complete your "
                                      "registration. It's easy - just check your email and click on the confirmation "
                                      "link.")
            return redirect(reverse('homepage'))
    else:
        register_form = UserRegistrationForm()
    login_form = UserAuthForm(request)
    context = {
        'register_form': register_form,
        'login_form': login_form
    }
    return render(request, 'accounts/login.html', context)


@login_required
def create_password(request):
    if request.method == 'POST':
        password_form = UserPasswordSetupForm(request.POST)
        if password_form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user.set_password(password_form.cleaned_data['password1'])

            messages.success(request, "Password was successfully set. Please, log in again")
            user.save()
            return redirect(reverse('personal_information'))
    else:
        password_form = UserPasswordSetupForm()
    context = {
        'form': password_form
    }
    return render(request, 'accounts/password_create_form.html', context)


def logout_view(request):
    _next = request.GET.get('next')
    logout(request)
    return redirect(_next if _next else settings.LOGOUT_REDIRECT_URL)


def activate_view(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and TokenGenerator().check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, "Thank you for confirming your email!")
        return redirect(reverse('index'))
    return HttpResponse('Activation link is invalid!')
