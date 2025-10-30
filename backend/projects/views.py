from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for listing and retrieving projects.
    For now, it shows all projects for quick sanity checks.
    We'll restrict by owner in the next step.
    """
    queryset = Project.objects.all().order_by("-created_at")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]  # keep open for initial testing

