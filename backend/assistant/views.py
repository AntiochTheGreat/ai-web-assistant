from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from .serializers import AskSerializer, DialogSerializer, MessageSerializer
from .services.ai_client import ask_ai
from .models import Dialog, Message
from projects.models import Project


class IsProjectOwner(permissions.BasePermission):
    """Allow access only to objects belonging to the current user's projects."""

    def has_object_permission(self, request, view, obj):
        # Dialog -> project.owner
        if isinstance(obj, Dialog):
            return obj.project.owner == request.user
        # Message -> dialog.project.owner
        if isinstance(obj, Message):
            return obj.dialog.project.owner == request.user
        return False


class DialogViewSet(viewsets.ModelViewSet):
    """
    CRUD for dialogs that belong to the current user's projects.
    """
    serializer_class = DialogSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        # Only dialogs from projects owned by the current user
        return Dialog.objects.filter(project__owner=self.request.user).order_by("-updated_at")

    def perform_create(self, serializer):
        # Ensure user owns the project
        project = serializer.validated_data["project"]
        if project.owner != self.request.user:
            raise permissions.PermissionDenied("You do not own this project.")
        serializer.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    CRUD for messages inside dialogs that belong to the current user.
    For now, we mostly care about listing and creating.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        return Message.objects.filter(
            dialog__project__owner=self.request.user
        ).select_related("sender", "dialog").order_by("created_at")

    def perform_create(self, serializer):
        dialog = serializer.validated_data["dialog"]
        if dialog.project.owner != self.request.user:
            raise permissions.PermissionDenied("You do not own this dialog.")
        serializer.save(
            sender=self.request.user,
            role=Message.ROLE_USER,
        )


class AskView(APIView):
    """
    Forwards prompt to the ai_service microservice and stores dialog/messages.

    Behaviour:
    - project_id (required): must belong to current user
    - dialog_id (optional): if provided, message is appended to this dialog
      (must belong to given project & user)
    - if dialog_id is not provided, a new dialog is created
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=AskSerializer,
        responses={200: OpenApiTypes.OBJECT},
    )

    def post(self, request):
        serializer = AskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Validate project ownership
        project = get_object_or_404(
            Project,
            id=data["project_id"],
            owner=request.user,
        )

        # Find or create dialog
        dialog = None
        if dialog_id := data.get("dialog_id"):
            dialog = get_object_or_404(
                Dialog,
                id=dialog_id,
                project=project,
            )
        else:
            dialog = Dialog.objects.create(
                project=project,
                title=data["prompt"][:80],
            )

        prompt = data["prompt"].strip()
        if not prompt:
            return Response(
                {"detail": "Prompt cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Store user message
        Message.objects.create(
            dialog=dialog,
            sender=request.user,
            role=Message.ROLE_USER,
            content=prompt,
        )

        # Call AI microservice
        result = ask_ai({
            "prompt": prompt,
            "project_id": project.id,
            "user": request.user.username,
        })

        answer = result.get("answer", "")

        # Store assistant message
        Message.objects.create(
            dialog=dialog,
            sender=None,
            role=Message.ROLE_ASSISTANT,
            content=answer,
        )

        # Return answer + dialog id
        return Response(
            {
                "answer": answer,
                "dialog_id": dialog.id,
                "project_id": project.id,
            },
            status=status.HTTP_200_OK,
        )
