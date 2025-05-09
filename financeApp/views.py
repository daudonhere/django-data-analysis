from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse
from financeApp.serializers import StockDataSerializer, MarketActiveStockSerializer, SectorPerformanceSerializer, CryptoSymbolSerializer, TopLoserStockSerializer
import os
import requests
from dotenv import load_dotenv

load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE_URL = os.getenv("FMP_BASE_URL")

class FinancialDataViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Most Searched Stocks",
        description="Returns a list of the most searched stocks",
        tags=["Economics & Finance"],
        responses={
            200: OpenApiResponse(
                response=StockDataSerializer(many=True),
                description="Returns a list of the most searched stocks",
            ),
            500: OpenApiResponse(description="Internal Server Error"),
        },
    )
    @action(detail=False, methods=["get"], url_path="stocks")
    def get_stock_list(self, request):
        url = f"{FMP_BASE_URL}/stock/list?apikey={FMP_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            raw_data = response.json()[:100]
            serializer = StockDataSerializer(data=raw_data, many=True)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @extend_schema(
        summary="Market Highest Volume",
        description="Returns a list of stocks with highest trading volume",
        tags=["Economics & Finance"],
        responses={
            200: OpenApiResponse(
                response=MarketActiveStockSerializer(many=True),
                description="List of high volume stocks",
            ),
            500: OpenApiResponse(description="Internal Server Error"),
        },
    )
    @action(detail=False, methods=["get"], url_path="volume")
    def get_market_highest_volume(self, request):
        url = f"{FMP_BASE_URL}/stock_market/actives?apikey={FMP_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            raw_data = response.json()

            serializer = MarketActiveStockSerializer(data=raw_data, many=True)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @extend_schema(
        summary="Most Sector Performance",
        description="Returns performance change for each sector",
        tags=["Economics & Finance"],
        responses={
            200: OpenApiResponse(
                response=SectorPerformanceSerializer(many=True),
                description="List of sector performance data",
            ),
            500: OpenApiResponse(description="Internal Server Error"),
        },
    )
    @action(detail=False, methods=["get"], url_path="sector")
    def get_sector_performance(self, request):
        url = f"{FMP_BASE_URL}/sector-performance?apikey={FMP_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            raw_data = response.json().get("sectorPerformance", [])

            serializer = SectorPerformanceSerializer(data=raw_data, many=True)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @extend_schema(
        summary="Most Traded Cryptocurrencies",
        description="Returns a list of most traded cryptocurrency",
        tags=["Economics & Finance"],
        responses={
            200: OpenApiResponse(
                response=CryptoSymbolSerializer(many=True),
                description="List of available crypto assets",
            ),
            500: OpenApiResponse(description="Internal Server Error"),
        },
    )
    @action(detail=False, methods=["get"], url_path="crypto")
    def get_crypto_symbols(self, request):
        url = f"{FMP_BASE_URL}/symbol/available-cryptocurrencies?apikey={FMP_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            raw_data = response.json()[:100]

            serializer = CryptoSymbolSerializer(data=raw_data, many=True)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @extend_schema(
        summary="Most Stocks Downtrend",
        description="Returns a list of stocks with the highest negative price changes",
        tags=["Economics & Finance"],
        responses={
            200: OpenApiResponse(
                response=TopLoserStockSerializer(many=True),
                description="List of top downtrend stocks",
            ),
            500: OpenApiResponse(description="Internal Server Error"),
        },
    )
    @action(detail=False, methods=["get"], url_path="downtrend")
    def get_top_losers(self, request):
        url = f"{FMP_BASE_URL}/stock_market/losers?apikey={FMP_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            raw_data = response.json()[:100]

            serializer = TopLoserStockSerializer(data=raw_data, many=True)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

