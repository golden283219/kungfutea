from django.core.exceptions import ValidationError
from rest_framework import mixins, viewsets, status
from push_notifications.models import APNSDevice, GCMDevice
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import NotificationSerializer


class NotificationViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    http_method_names = (
        "get",
        "post",
    )
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     devices = []
    #     for model in [GCMDevice, APNSDevice]:
    #         devices.extend(
    #             list(
    #                 model.objects.filter(user=self.request.user).values(
    #                     "device_id", "application_id", "registration_id"
    #                 )
    #             )
    #         )

    #     return devices
    # # read notification
    # def get_object(self):
    #     try:
    #         gcm_device = GCMDevice.objects.filter(
    #             device_id=int(self.kwargs["pk"])
    #         ).first()
    #     except (ValidationError, ValueError):
    #         gcm_device = None

    #     try:
    #         apns_device = APNSDevice.objects.filter(device_id=self.kwargs["pk"]).first()
    #     except ValidationError:
    #         apns_device = None

    #     if apns_device:
    #         return apns_device
    #     elif gcm_device:
    #         return gcm_device
    # # make notification 
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     if serializer.data["application_id"] == "ios_app":
    #         APNSDevice.objects.filter(**serializer.data).delete()
    #         APNSDevice.objects.create(user=request.user, **serializer.data)
    #     else:
    #         GCMDevice.objects.filter(
    #             cloud_message_type="FCM", **serializer.data
    #         ).delete()
    #         GCMDevice.objects.create(
    #             user=request.user, cloud_message_type="FCM", **serializer.data
    #         )

    #     headers = self.get_success_headers(serializer.data)
    #     return Response(
    #         serializer.data, status=status.HTTP_201_CREATED, headers=headers
    #     )
    
    def get_queryset(self):
        devices = []
        for model in [GCMDevice, APNSDevice]:
            devices.extend(
                list(
                    model.objects.filter(user=self.request.user).values(
                        "device_id", "application_id", "registration_id"
                    )
                )
            )

        return devices
    # read notification
    def get_object(self):
        try:
            gcm_device = GCMDevice.objects.filter(
                device_id=int(self.kwargs["pk"])
            ).first()
        except (ValidationError, ValueError):
            gcm_device = None

        try:
            apns_device = APNSDevice.objects.filter(device_id=self.kwargs["pk"]).first()
        except ValidationError:
            apns_device = None

        if apns_device:
            return apns_device
        elif gcm_device:
            return gcm_device
    # make notification 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.data["application_id"] == "ios_app":
            APNSDevice.objects.filter(**serializer.data).delete()
            APNSDevice.objects.create(user=request.user, **serializer.data)
        else:
            GCMDevice.objects.filter(
                cloud_message_type="FCM", **serializer.data
            ).delete()
            GCMDevice.objects.create(
                user=request.user, cloud_message_type="FCM", **serializer.data
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
