from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import SetupGmailClientView, AnnouncementViewSet, TrackAnnouncementViewTime

router = SimpleRouter()
router.register("announcements", AnnouncementViewSet, basename="announcement")

urlpatterns = [
    path("oauth/gmail/", SetupGmailClientView.as_view()),
    path("track-time/<str:pk>/", TrackAnnouncementViewTime.as_view()),
] + router.urls
