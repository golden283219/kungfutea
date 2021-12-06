from rest_framework import serializers

# dipatch notification
class NotificationSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=64)
    application_id = serializers.ChoiceField(choices=["ios_app", "android_app"])
    registration_id = serializers.CharField(max_length=2048)
