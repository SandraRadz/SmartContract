from django.urls import path, re_path, reverse_lazy, include
from django.contrib.auth import views as auth_views

from accounts.views import activate_view
from . import views
from django.conf import settings

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('password-create/', views.create_password, name='password_create'),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
        ),
        name='password_change'),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/personal_information.html',
            extra_context={'extra_message': 'Password was successfully changed'}
        ),
        name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        email_template_name='accounts/email/password_reset.html',
        subject_template_name='accounts/email/password_reset_subject.txt',
        template_name='accounts/password_reset.html',
        success_url=reverse_lazy('password_reset_done'),
        extra_email_context={'domain': settings.APP_DOMAIN},
        html_email_template_name='accounts/email/password_reset.html',
    ),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
    ), name='password_reset_done'),
    re_path(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ), name='password_reset_confirm'),
    re_path(
        r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_complete.html',
        ),
        name='password_reset_complete'),

    path('my-account/', views.personal_information, name='personal_information'),
    path('my-account/edit/', views.edit_personal_information, name='edit_personal_information'),
    path('activate/<uidb64>/<token>', activate_view, name='activate')
]
