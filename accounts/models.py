from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.signals import pre_save, post_delete, post_save
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """
    Creates and saves a User with the given email, phone, password and optional extra info.
    """

    def _create_user(self, email,
                     first_name, last_name,
                     password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff, is_active=True,
            is_verified=False,
            is_superuser=is_superuser,
            date_joined=now,
            last_login=now,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name=None, last_name=None, password=None, **extra_fields):
        return self._create_user(email, first_name, last_name, password, False, False, **extra_fields)

    def create_superuser(
            self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email,
        name and password.
        """
        return self._create_user(email, first_name, last_name, password, True, True, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)


class UserStatus(models.TextChoices):
    DEFAULT = "default", "DEFAULT"
    REQUEST_SOLVER = "request_solver", "REQUEST_SOLVER"
    SOLVER = "solver", "SOLVER"


class User(AbstractBaseUser, PermissionsMixin):
    """
    A model which implements the authentication model.

    Email and password are required. Other fields are optional.

    Email field are used for logging in.
    """
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    first_name = models.CharField(_('First name'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(
        _('verify status'),
        default=False,
        help_text=_('Designates whether the user has verified his email.'), )
    status = models.CharField(max_length=20, choices=UserStatus.choices, default=UserStatus.DEFAULT)
    # escrow_hash = models.CharField(max_length=255, blank=True, default="")
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['first_name', 'last_name', '-date_joined']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_email_md5_hash(self):
        import hashlib
        m = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return m

    def has_usable_password(self) -> bool:
        return super().has_usable_password()

    def default_user(self):
        return self.status == "default"

    has_usable_password.boolean = True

    @property
    def days_on_site(self):
        from django.utils.timezone import now
        delta = now() - self.date_joined
        return delta.days

