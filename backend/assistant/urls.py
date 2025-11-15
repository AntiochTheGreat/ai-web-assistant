from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AskView, DialogViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"dialogs", DialogViewSet, basename="dialog")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("ask/", AskView.as_view(), name="assistant-ask"),
    path("", include(router.urls)),
]
