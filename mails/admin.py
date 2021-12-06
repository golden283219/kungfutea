import time
from django.contrib import admin
from django.contrib.auth.models import Group
from push_notifications.models import APNSDevice, GCMDevice, WNSDevice, WebPushDevice
from rest_framework.authtoken.models import Token

from .models import Announcement, AnnouncementViewModel


admin.site.unregister(APNSDevice)
admin.site.unregister(GCMDevice)
admin.site.unregister(WNSDevice)
admin.site.unregister(WebPushDevice)
admin.site.unregister(Token)
admin.site.unregister(Group)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "internal_date")
    ordering = ("-internal_date",)
    search_fields = ("snippet", "internal_date")


@admin.register(AnnouncementViewModel)
class AnnouncementViewModel(admin.ModelAdmin):
    list_display = ("user", "announcement", "view_time_seconds")
    autocomplete_fields = ("user", "announcement")
    search_fields = ("user__email",)
    readonly_fields = ("view_time",)
    list_filter = ("announcement",)

    def view_time(self, instance):
        return time.strftime("%H:%M:%S", time.gmtime(instance.view_time_seconds))
