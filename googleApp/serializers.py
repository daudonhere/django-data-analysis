from rest_framework import serializers

class TrendingSearchesSerializer(serializers.Serializer):
    region = serializers.CharField(required=False, default='global')

class InterestOverTimeSerializer(serializers.Serializer):
    keywords = serializers.ListField(
        child=serializers.CharField(), 
        required=True, 
        allow_empty=False
    )
