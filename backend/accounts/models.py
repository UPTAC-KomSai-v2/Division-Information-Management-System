from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import os


def user_avatar_path(instance, filename):
    """Generate upload path for user avatars"""
    # Upload to: media/avatars/{user_id}/{filename}
    return os.path.join('avatars', str(instance.id), filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    # no username field
    email = models.EmailField(unique=True)

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Division Admin"
        STAFF = "STAFF", "Staff"
        FACULTY = "FACULTY", "Faculty/Stakeholder"

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.STAFF,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Profile fields
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class UserStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        ON_LEAVE = "ON_LEAVE", "On Leave"

    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
    )

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # we only ask for email + password

    objects = UserManager()  # ✅ IMPORTANT

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.get_full_name()} ({self.email})"
        return f"{self.email} ({self.role})"

    def get_full_name(self):
        """Return the full name of the user"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        if full_name:
            return full_name

        # Backend-defined display names for known accounts
        overrides = {
            "matt@yahoo.com": "Matthew Dalomias",
            "admin@test.com": "Administrator 1",
            "admin@dims.com": "Administrator 2",
        }
        email_lower = (self.email or "").lower()
        if email_lower in overrides:
            return overrides[email_lower]

        # Otherwise, fall back to email local-part before using full email
        if email_lower and "@" in email_lower:
            return email_lower.split("@")[0]
        return self.email

    def get_short_name(self):
        """Return the short name of the user"""
        return self.first_name if self.first_name else self.email

    @property
    def initials(self):
        """Generate initials from first and last name"""
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        elif self.first_name:
            return self.first_name[0].upper()
        elif self.email:
            return self.email[0].upper()
        return "U"
