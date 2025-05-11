from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from pytrends.request import TrendReq
from googleApp.serializers import TrendingTopicSerializer

class GoogleTrendViewSet(viewsets.ViewSet):
    pytrends = TrendReq(hl='en-US', tz=360)

    @extend_schema(
        summary="Trending Topics Based on Topic and Region",
        description="Returns most searched trends based on a given topic and region (country code).",
        tags=["Google Trends"],
        parameters=[
            OpenApiParameter(name="topic", description="Search topic/category (default: 'finance')", required=False, type=str),
            OpenApiParameter(name="region", description="2-letter country code (e.g. US, JP, ID). Leave empty for global.", required=False, type=str),
        ],
        responses={
            200: OpenApiResponse(response=TrendingTopicSerializer(many=True)),
            500: OpenApiResponse(description="Internal Server Error")
        }
    )
    @action(detail=False, methods=["get"], url_path="trending-topic")
    def trending_topic(self, request):
        topic_query = request.query_params.get("topic", "finance")
        region = request.query_params.get("region", "")

        try:
            suggestions = self.pytrends.suggestions(keyword=topic_query)
            if not suggestions:
                return Response({"error": "No keyword suggestions found for topic."}, status=204)

            selected = suggestions[0]
            topic_mid = selected["mid"]
            topic_title = selected["title"]

            self.pytrends.build_payload(
                kw_list=[topic_mid],
                timeframe='now 7-d',
                geo=region,
                gprop=""
            )

            df = self.pytrends.interest_over_time()
            if df.empty:
                return Response({"error": "No data returned from Google Trends."}, status=204)

            trends_data = []
            for date, row in df.iterrows():
                if topic_mid not in row or row[topic_mid] is None:
                    continue

                trends_data.append({
                    "trend": topic_title,
                    "value": row[topic_mid],
                    "startFrom": date.isoformat(),
                    "volume": f"{int(row[topic_mid]) * 1000}+",
                    "region": region or "global",
                    # "category": topic_mid,
                    "source": "Google Trends"
                })

            serializer = TrendingTopicSerializer(data=trends_data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": f"Exception: {str(e)}"}, status=500)
