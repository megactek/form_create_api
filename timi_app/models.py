from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

STATE_CHOICES = (
    ("abia", "abia"),
    ("kogin", "kogi"),
    ("lagos", "lagos"),
    ("ondo", "ondo"),
    ("osun", "osun"),
)


class Address(models.Model):
    street = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=10, choices=STATE_CHOICES)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_active", True)
        if kwargs.get("is_superuser"):
            raise Exception("user cannot have is_superuser=False")
        if kwargs.get("is_staff"):
            raise Exception("user cannot have is_staff=False")
        if not kwargs.get("is_active"):
            raise Exception("user cannot have is_active=True")

        user = self.model(
            email=email,
            **kwargs,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)

        if not kwargs.get("is_superuser"):
            raise Exception("superuser cannot have is_superuser=False")
        if not kwargs.get("is_staff"):
            raise Exception("superuser cannot have is_staff=False")
        if not kwargs.get("is_active"):
            raise Exception("superuser cannot have is_active=False")

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, unique=True, null=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(
        Address,
        related_name="user_address",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    last_login = models.DateTimeField(null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("username",)
