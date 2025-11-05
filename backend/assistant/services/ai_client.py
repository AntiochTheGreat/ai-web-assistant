"""Synchronous client for talking to the ai_service."""
import httpx
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException

class UpstreamUnavailable(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "AI service is unavailable."
    default_code = "upstream_unavailable"

def ask_ai(payload: dict) -> dict:
    """
    Calls the FastAPI microservice /ask endpoint and returns JSON.
    Raises httpx.HTTPError on network/protocol errors.
    """
    url = f"{settings.AI_SERVICE_URL}/ask"
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        # network / DNS / refused
        raise UpstreamUnavailable(f"AI service connection error: {e}") from e
    except httpx.HTTPStatusError as e:
        # non-2xx from upstream
        raise UpstreamUnavailable(f"AI service error {e.response.status_code}: {e.response.text}") from e
