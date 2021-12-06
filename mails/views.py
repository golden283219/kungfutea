from apiclient import discovery
import httplib2
from oauth2client import client
from django.conf import settings
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from django.utils.translation import ugettext as _

from mails.models import Announcement, AnnouncementViewModel
from mails.serializers import AnnouncementDetailSerializer, AnnouncementListSerializer
from notifications.utils import send_push_notifications


class SetupGmailClientView(APIView):
    def get(self, request, *args, **kwargs):
        # If this request does not have `X-Requested-With` header, this could be a CSRF
        if not request.headers.get("X-Requested-With"):
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Set path to the Web application client_secret_*.json file you downloaded from the
        # Google API Console: https://console.developers.google.com/apis/credentials

        # Exchange auth code for access token, refresh token, and ID token
        credentials = client.credentials_from_clientsecrets_and_code(
            settings.CLIENT_SECRET_FILE,
            ["https://www.googleapis.com/auth/drive.appdata", "profile", "email"],
            request["auth_code"],
        )

        # Call Google API
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build("drive", "v3", http=http_auth)
        appfolder = drive_service.files().get(fileId="appfolder").execute()

        # Get profile info from ID token
        user_id = credentials.id_token["sub"]
        email = credentials.id_token["email"]

        return Response(status=status.HTTP_200_OK)


class AnnouncementViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    http_method_names = ("get",)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.all().order_by("-internal_date")

    def get_serializer_class(self):
        if self.action == "list":
            return AnnouncementListSerializer
        elif self.action == "retrieve":
            return AnnouncementDetailSerializer

    # TODO: remove this temp endpoint
    @action(detail=True, methods=["get"])
    def push_notification(self, request, *args, **kwargs):
        send_push_notifications(
            request.user,
            _("You got a new announcement."),
            thread_id="tkk_application_new_announcement",
            event_type="announcement_new",
            announcement_id=self.kwargs["pk"],
        )

        return Response(status=status.HTTP_200_OK)


class TrackAnnouncementViewTime(APIView):
    http_method_names = ("get",)
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Announcement, id=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        announcement_view_model, _ = AnnouncementViewModel.objects.get_or_create(
            user=request.user, announcement=self.get_object()
        )
        announcement_view_model.view_time_seconds += 1
        announcement_view_model.save()

        return Response(status=status.HTTP_200_OK)
