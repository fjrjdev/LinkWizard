from rest_framework import serializers


class CrawledDataSerializer(serializers.Serializer):
    url = serializers.URLField()
    label = serializers.CharField(max_length=255)
