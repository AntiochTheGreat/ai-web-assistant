from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import AskSerializer

class AskView(APIView):
    """Stub endpoint that echoes back the prompt.

    In later steps we'll call the ai_service microservice from here.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Very simple stubbed logic (no AI yet)
        prompt = data["prompt"].strip()
        if not prompt:
            return Response({"detail": "Prompt cannot be empty."},
                            status=status.HTTP_400_BAD_REQUEST)

        reply = f"Echo: {prompt}"

        return Response({
            "answer": reply,
            "project_id": data.get("project_id"),
            "user": request.user.username
        }, status=status.HTTP_200_OK)
