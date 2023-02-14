from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from project.constants import UserAccountType


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        if extra_fields.get("dni"):
            user.dni = extra_fields.get("dni")
        if extra_fields.get("account_type"):
            user.account_type = extra_fields.get("account_type")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    account_type = models.IntegerField(
        choices=UserAccountType.choices, default=UserAccountType.PATIENT
    )
    institutional_id = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    dni = models.CharField(max_length=20, unique=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    expiration_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
