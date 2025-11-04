from rest_framework import serializers

class AskSerializer(serializers.Serializer):
    """Minimal payload to ask the assistant."""
    prompt = serializers.CharField()
    project_id = serializers.IntegerField(required=False)
