from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    name_of_the_expert = serializers.CharField(source="seller.get_full_name", read_only=True)
    merchant_id = serializers.CharField(source="seller.merchant_id", read_only=True)

    class Meta:
        model = Service
        fields = (
            "id",
            "seller",
            "service_name",
            "description",
            "rating",
            "price",
            "duration_of_service",
            "sample_image",
            "name_of_the_expert",
            "merchant_id",
        )
        read_only_fields = ("id", "seller", "name_of_the_expert")
