from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
ALPHA_BASE_URL = os.getenv("ALPHA_BASE_URL")

class AnalyticSentimentViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Most Trend Topics About Fiscal Economics Policy",
        description="Returns fiscal economic data analysis.",
        tags=["Economy & Finances"],
        responses={
            200: OpenApiResponse(description="Success Response."),
            500: OpenApiResponse(description="Internal Server Error")
        }
    )
    @action(detail=False, methods=["get"], url_path="fiscal")
    def get_economy_fiscal_sentiment(self, request):
        url = f"{ALPHA_BASE_URL}/query?function=NEWS_SENTIMENT&apikey={ALPHA_API_KEY}&topics=economy_fiscal"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    @extend_schema(
        summary="Data Monetary Economics and Public Responses",
        description="Returns monetary economic data analysis.",
        tags=["Economy & Finances"],
        responses={
            200: OpenApiResponse(description="Success Response"),
            500: OpenApiResponse(description="Internal Server Error")
        }
    )
    @action(detail=False, methods=["get"], url_path="monetary")
    def get_economy_monetary_sentiment(self, request):
        url = f"{ALPHA_BASE_URL}/query?function=NEWS_SENTIMENT&apikey={ALPHA_API_KEY}&topics=economy_monetary"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @extend_schema(
        summary="Most Trend About Macro Economics",
        description="Return macro economic data analysis and public response",
        tags=["Economy & Finances"],
        responses={
            200: OpenApiResponse(description="Success Response"),
            500: OpenApiResponse(description="Internal Server Error")
        }
    )
    @action(detail=False, methods=["get"], url_path="macro")
    def get_economy_macro_sentiment(self, request):
        url = f"{ALPHA_BASE_URL}/query?function=NEWS_SENTIMENT&apikey={ALPHA_API_KEY}&topics=economy_macro"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
