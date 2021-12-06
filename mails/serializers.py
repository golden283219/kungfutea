from rest_framework import serializers

from .models import Announcement, AnnouncementViewModel


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = (
            "id",
            "label_ids",
            "snippet",
            "internal_date",
            "title",
            "body",
        )


class AnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = (
            "id",
            "label_ids",
            "snippet",
            "internal_date",
            "title",
        )
