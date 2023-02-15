from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from project.constants import UserAccountType


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, dni=None, account_type=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not dni:
            raise ValueError("Users must have a dni")
            # if not password, generate a random password
        if not password:
            password = self.make_random_password()

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.dni = dni
        user.account_type = account_type
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, dni="00000000")
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
    institution = models.ForeignKey(
        "Institution", on_delete=models.SET_NULL, null=True, blank=True
    )
    institutional_id = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    dni = models.CharField(max_length=20, unique=True)
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


class Institution(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
