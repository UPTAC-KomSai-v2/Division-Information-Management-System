from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


# =========================
# Role & User Management
# =========================


class Role(models.Model):
    """
    Role table with ADMIN, STAFF, FACULTY.
    Seed with:
    - ADMIN
    - STAFF
    - FACULTY
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name


class Unit(models.Model):
    """
    Organizational unit (e.g., division, department, office).
    """
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    """
    Custom user manager using email as username.
    Now supports firstname, lastname, role, and unit.
    """

    def create_user(self, email, firstname, lastname, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            firstname=firstname,
            lastname=lastname,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname="Super", lastname="User", password=None, **extra_fields):
        """
        Automatically assigns:
        - is_staff = True
        - is_superuser = True
        - role = ADMIN (must exist in Role table)
        """

        from .models import Role  # avoid circular import
        admin_role = Role.objects.get(name="ADMIN")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", admin_role)

        return self.create_user(
            email=email,
            firstname=firstname,
            lastname=lastname,
            password=password,
            **extra_fields
        )

# class UserManager(BaseUserManager):
#     """
#     Custom user manager using email as the username field.
#     """

#     def create_user(self, email, firstname, lastname, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Users must have an email address")

#         email = self.normalize_email(email)
#         user = self.model(
#             email=email,
#             firstname=firstname,
#             lastname=lastname,
#             **extra_fields,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, firstname="Admin", lastname="User", password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("is_active", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self.create_user(email, firstname, lastname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model:
    - email as unique identifier
    - firstname, lastname
    - FK to Role and Unit
    """
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # required by Django admin
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.firstname} {self.lastname} <{self.email}>"


# =========================  


# Memos & Routing
# =========================


class Memo(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        NORMAL = "NORMAL", "Normal"
        HIGH = "HIGH", "High"

    title = models.CharField(max_length=255)
    body = models.TextField()
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )
    requires_ack = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_memos",
    )
    target_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="memos",
    )

    class Meta:
        verbose_name = "Memo"
        verbose_name_plural = "Memos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.priority}] {self.title}"


class MemoRoute(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACKNOWLEDGED = "ACKNOWLEDGED", "Acknowledged"

    memo = models.ForeignKey(
        Memo,
        on_delete=models.CASCADE,
        related_name="routes",
    )
    # per your instruction: name string, not FK
    recipient_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    class Meta:
        verbose_name = "Memo Route"
        verbose_name_plural = "Memo Routes"

    def __str__(self):
        return f"{self.recipient_name} - {self.memo.title} ({self.status})"


# =========================
# Documents & Versions
# =========================


class Document(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="owned_documents",
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        related_name="documents",
        null=True,
        blank=True,
    )

    # convenience pointer to latest version
    current_version = models.OneToOneField(
        "DocumentVersion",
        on_delete=models.SET_NULL,
        related_name="current_for_document",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class DocumentVersion(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="versions",
    )
    file_path = models.FileField(upload_to="documents/")
    file_size = models.BigIntegerField()
    integrity_hash = models.CharField(max_length=64)  # SHA-256 hex
    version_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="uploaded_document_versions",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Document Version"
        verbose_name_plural = "Document Versions"
        ordering = ["-created_at"]
        unique_together = ("document", "version_number")

    def __str__(self):
        return f"{self.document.title} v{self.version_number}"


# =========================
# Tickets & Updates
# =========================


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sla_due_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tickets",
    )
    assigned_unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        related_name="tickets",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.id} {self.title} ({self.status})"


class TicketUpdate(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="updates",
    )
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="ticket_updates",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Ticket Update"
        verbose_name_plural = "Ticket Updates"
        ordering = ["created_at"]

    def __str__(self):
        return f"Ticket #{self.ticket_id} {self.old_status} → {self.new_status}"


# =========================
# Events & Announcements
# =========================


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="created_events",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ["start_at"]

    def __str__(self):
        return f"{self.title} @ {self.start_at}"


class Announcement(models.Model):
    class Category(models.TextChoices):
        SYSTEM = "SYSTEM", "System"
        GENERAL = "GENERAL", "General"
        ALERT = "ALERT", "Alert"

    title = models.CharField(max_length=255)
    body = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.GENERAL,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="created_announcements",
        null=True,
        blank=True,
    )
    # NULL target_unit = division-wide
    target_unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        related_name="announcements",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# =========================
# Notifications
# =========================


class Notification(models.Model):
    """
    Persistent notifications for users.

    Works together with WebSockets:
    - row is created whenever an important event happens
    - WebSocket pushes the event in real time
    - UI can query unread notifications from DB later
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()  # small snapshot of the event
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification to {self.user} ({self.event_type})"