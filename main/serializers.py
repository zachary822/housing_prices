from rest_framework import serializers

from .models import Sale


class SaleSerializer(serializers.ModelSerializer):
    neighborhood = serializers.StringRelatedField()
    borough = serializers.StringRelatedField(source="neighborhood.borough")

    class Meta:
        model = Sale
        fields = ['borough', 'neighborhood', 'id', 'address', 'price', 'date']
