from rest_framework import serializers
from .models import SopAndPosLink

class SopAndPosLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SopAndPosLink
        fields = ("SOP_link", "POS_link")
        # fields = '__all__'