from rest_framework import serializers

class StockDataSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    name = serializers.CharField()
    price = serializers.FloatField()
    exchange = serializers.CharField()
    exchangeShortName = serializers.CharField()
    type = serializers.CharField()
    
class MarketActiveStockSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    name = serializers.CharField()
    change = serializers.FloatField()
    price = serializers.FloatField()
    changesPercentage = serializers.FloatField()
    
class SectorPerformanceSerializer(serializers.Serializer):
    sector = serializers.CharField()
    changesPercentage = serializers.CharField()
    
class CryptoSymbolSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    name = serializers.CharField()
    currency = serializers.CharField()
    stockExchange = serializers.CharField()
    exchangeShortName = serializers.CharField()
    
class TopLoserStockSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    name = serializers.CharField()
    change = serializers.FloatField()
    price = serializers.FloatField()
    changesPercentage = serializers.FloatField()



