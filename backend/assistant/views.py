from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import AskSerializer
from .services.ai_client import ask_ai

class AskView(APIView):
    """Forwards prompt to the ai_service microservice."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        prompt = data["prompt"].strip()
        if not prompt:
            return Response({"detail": "Prompt cannot be empty."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Forward to ai_service
        result = ask_ai({
            "prompt": prompt,
            "project_id": data.get("project_id"),
            "user": request.user.username,
        })

        return Response(result, status=status.HTTP_200_OK)
