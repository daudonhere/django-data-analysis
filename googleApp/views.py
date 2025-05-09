import os
import requests
from dotenv import load_dotenv
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter

load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE_URL = os.getenv("FMP_BASE_URL")


class FinancialDataViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Get latest 10 economic highlights",
        tags=["Financial Modeling Prep"],
        responses={200: dict}
    )
    @action(detail=False, methods=["get"], url_path="highlights")
    def get_highlights(self, request):
        url = f"{FMP_BASE_URL}/stock_news?limit=10&apikey={FMP_API_KEY}"
        try:
            res = requests.get(url)
            return Response(res.json())
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Filter by country, asset, or company",
        tags=["Financial Modeling Prep"],
        parameters=[
            OpenApiParameter(name='query', required=True, type=str, description='Filter by keyword like country, company, or asset')
        ],
        responses={200: dict}
    )
    @action(detail=False, methods=["get"], url_path="filter")
    def filter_data(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Query parameter is required"}, status=400)

        url = f"{FMP_BASE_URL}/search?query={query}&limit=10&apikey={FMP_API_KEY}"
        try:
            res = requests.get(url)
            return Response(res.json())
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @extend_schema(
        summary="Get stable assets or stocks over time",
        tags=["Financial Modeling Prep"],
        responses={200: dict}
    )
    @action(detail=False, methods=["get"], url_path="stable")
    def get_stable(self, request):
        url = f"{FMP_BASE_URL}/stock_market/gainers?apikey={FMP_API_KEY}"
        try:
            res = requests.get(url)
            return Response(res.json())
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @extend_schema(
        summary="Get categorized trend or class data (for charting)",
        tags=["Financial Modeling Prep"],
        parameters=[
            OpenApiParameter(name='symbol', required=True, type=str, description='Symbol of the asset')
        ],
        responses={200: dict}
    )
    @action(detail=False, methods=["get"], url_path="chart-data")
    def chart_data(self, request):
        symbol = request.query_params.get("symbol")
        if not symbol:
            return Response({"error": "Symbol is required"}, status=400)

        url = f"{FMP_BASE_URL}/historical-price-full/{symbol}?timeseries=7&apikey={FMP_API_KEY}"
        try:
            res = requests.get(url)
            return Response(res.json())
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @extend_schema(
        summary="Search categorized economic trend score",
        tags=["Financial Modeling Prep"],
        request={
            'application/json': {
                'example': {
                    'keyword': 'bitcoin'
                }
            }
        },
        responses={200: dict}
    )
    @action(detail=False, methods=["post"], url_path="search-trend")
    def search_trend(self, request):
        keyword = request.data.get('keyword')
        if not keyword:
            return Response({"error": "Keyword is required"}, status=400)

        url = f"{FMP_BASE_URL}/search?query={keyword}&limit=1&apikey={FMP_API_KEY}"
        try:
            res = requests.get(url)
            data = res.json()
            if not data:
                return Response({"message": "Not found in category"}, status=404)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
