from django.db import models
from django.conf import settings
from projects.models import Project


class Dialog(models.Model):
    """Represents a conversation thread inside a project."""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="dialogs",
    )
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title or f"Dialog #{self.pk}"


class Message(models.Model):
    """Single message in a dialog (user or assistant)."""
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ASSISTANT, "Assistant"),
    ]

    dialog = models.ForeignKey(
        Dialog,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
        help_text="User who sent the message (null for assistant).",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:50]}"
