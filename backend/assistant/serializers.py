from rest_framework import serializers
from .models import Dialog, Message
from projects.models import Project


class AskSerializer(serializers.Serializer):
    """Payload used to ask the assistant."""
    project_id = serializers.IntegerField()
    dialog_id = serializers.IntegerField(required=False)
    prompt = serializers.CharField()


class DialogSerializer(serializers.ModelSerializer):
    """Serializer for conversation dialogs."""
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source="project",
        write_only=True,
    )

    class Meta:
        model = Dialog
        fields = ["id", "project_id", "title", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for dialog messages."""
    sender_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "dialog", "role", "content", "created_at", "sender_username"]
        read_only_fields = ["id", "created_at", "sender_username", "role"]

    def get_sender_username(self, obj) -> str | None:
        if obj.sender:
            return obj.sender.username
        return None
