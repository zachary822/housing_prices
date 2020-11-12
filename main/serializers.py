from rest_framework import serializers

from .models import Sale


class SaleSerializer(serializers.ModelSerializer):
    neighborhood = serializers.StringRelatedField()
    borough = serializers.StringRelatedField(source="neighborhood.borough")
    date = serializers.DateTimeField(help_text="date of sale")

    class Meta:
        model = Sale
        fields = ['id', 'borough', 'neighborhood', 'address', 'price', 'date']


class SaleYearSerializer(serializers.Serializer):
    year = serializers.IntegerField(help_text="year of sales")
    avg = serializers.FloatField(help_text="average sale price")


class SummarySerializer(serializers.Serializer):
    result = SaleYearSerializer(many=True)
