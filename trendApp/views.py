from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from pytrends.request import TrendReq
from trendApp.serializers import TrendingTopicSerializer

class SearchTrendViewSet(viewsets.ViewSet):
    pytrends = TrendReq(hl='en-US', tz=360)

    @extend_schema(
        summary="Most Searched On The Internet",
        description="Showing the most search data trends on the internet related to economics and finance",
        tags=["Economy & Finances"],
        parameters=[
            OpenApiParameter(name="query", description="search query", required=True, type=str),
        ],
        responses={
            200: OpenApiResponse(response=TrendingTopicSerializer(many=True)),
            204: OpenApiResponse(description="There Is No Data For This Query"),
            400: OpenApiResponse(description="Query Parameter Is Required"),
            500: OpenApiResponse(description="An Error Occurred On The Server.")
        }
    )
    @action(detail=False, methods=["get"], url_path="search")
    def trending_topic(self, request):
        query = request.query_params.get("query")
        if not query:
            return Response({"error": "Query is required."}, status=400)

        try:
            category = 7
            timeframe = 'now 7-d'
            geo = ''
            gprop = ''

            self.pytrends.build_payload(
                kw_list=[query],
                cat=category,
                timeframe=timeframe,
                geo=geo,
                gprop=gprop
            )

            df = self.pytrends.interest_over_time()

            if df.empty or query not in df.columns:
                return Response({"error": f"There is no data for '{query}'."}, status=204)

            trend_data = []
            max_value = df[query].max()
            for date, row in df.iterrows():
                value = int(row[query])
                trend_data.append({
                    "trend": query,
                    "value": value,
                    "startFrom": date.isoformat(),
                    "volume": f"{value * 1000}",
                    "dayName": date.strftime('%A'),
                    "hour": date.hour,
                    "percentage": f"{round((value / max_value) * 100)}%",
                    "is_peak": value == max_value
                })

            serializer = TrendingTopicSerializer(data=trend_data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=200)

        except Exception as e:
            return Response({"error": f"Exception: {str(e)}"}, status=500)
