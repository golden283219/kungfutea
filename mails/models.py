from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from notifications.utils import send_push_notifications

User = get_user_model()


class Announcement(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    label_ids = ArrayField(
        models.CharField(max_length=64), default=list, blank=True, null=True,
    )
    snippet = models.TextField()
    internal_date = models.DateTimeField(_("Received Date (EST)"))

    title = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else self.id


@receiver(post_save, sender=Announcement)
def send_pushes(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all().iterator():
            send_push_notifications(
                user,
                _("You got a new announcement."),
                thread_id="tkk_application_new_announcement",
                event_type="announcement_new",
                announcement_id=instance.id,
            )


class AnnouncementViewModel(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)

    view_time_seconds = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Announcement View Report"
        verbose_name_plural = "Announcement View Reports"
