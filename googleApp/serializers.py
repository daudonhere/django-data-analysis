from rest_framework import serializers

class TrendingTopicSerializer(serializers.Serializer):
    trend = serializers.CharField(help_text="Topik atau kata kunci yang sedang tren")
    value = serializers.IntegerField(help_text="Nilai tren (0–100) yang merepresentasikan intensitas pencarian")
    startFrom = serializers.DateTimeField(help_text="Waktu mulai tren pada titik data ini")
    volume = serializers.CharField(help_text="Volume relatif pencarian (format teks untuk fleksibilitas)")
    region = serializers.CharField(help_text="Wilayah/negara tempat tren berasal (misal: 'JP' atau 'WORLD')")
    # category = serializers.CharField(help_text="Kategori utama atau kata kunci yang diminta (misal: 'finance')")
    source = serializers.CharField(help_text="Sumber data tren (misal: 'Google Trends')")
