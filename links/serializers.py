from rest_framework import serializers
from .models import Link
from users.serializers import UserSerializer


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["id", "label", "url"]


class LinkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"
