import logging

from django.core.exceptions import ImproperlyConfigured
from push_notifications.models import APNSDevice, GCMDevice

logger = logging.getLogger(__name__)


def send_push_notifications(user, body, thread_id="tkk_application", **kwargs):
    try:
        apns_devices = APNSDevice.objects.filter(user=user)
        gcm_devices = GCMDevice.objects.filter(user=user)

        apns_devices.send_message(body, thread_id=thread_id, extra=kwargs, badge=1)
        gcm_devices.send_message(body, thread_id=thread_id, extra=kwargs)

    except ImproperlyConfigured as e:
        logger.error(e)
