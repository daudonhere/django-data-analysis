from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from pytrends.request import TrendReq
from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers

# Serializer for endpoint "trending"
class RegionSerializer(serializers.Serializer):
    region = serializers.CharField(required=False, help_text="example: 'indonesia', 'united_states', dll. Default: 'global'")

# Serializer for endpoint "interest"
class KeywordsSerializer(serializers.Serializer):
    keywords = serializers.ListField(
        child=serializers.CharField(),
        help_text="keyword: ['python', 'django']"
    )

class GoogleTrendsViewSet(ViewSet):

    @extend_schema(
        summary="Get trending searches (POST)",
        request=RegionSerializer,
        responses={200: list}
    )
    @action(detail=False, methods=['post'], url_path='trending')
    def trending(self, request):
        region = request.data.get('region', 'global')
        try:
            pytrends = TrendReq()
            data = pytrends.trending_searches(pn=region) if region != 'global' else pytrends.trending_searches()
            return Response(data[0].tolist())
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Get interest over time (POST)",
        request=KeywordsSerializer,
        responses={200: dict}
    )
    @action(detail=False, methods=['post'], url_path='interest')
    def interest(self, request):
        keywords = request.data.get('keywords', [])
        if not keywords:
            return Response({"error": "Keywords parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pytrends = TrendReq()
            pytrends.build_payload(keywords, timeframe='now 7-d')
            data = pytrends.interest_over_time()
            return Response(data[keywords].to_dict(orient="list"))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
