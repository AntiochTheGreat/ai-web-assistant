from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer

class IsOwner(permissions.BasePermission):
    """Allow owners to access their own projects."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Authenticated CRUD for user's projects.
    - List only current user's projects
    - On create, owner is set to request.user
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
