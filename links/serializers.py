from rest_framework import serializers
from .models import MenuLink, QuickLink

class MenuLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuLink
        fields = ("Label", "Link", "BackButton")

class QuickLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = ("Label", "Link", "Icon", "BackButton")
