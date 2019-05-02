from rest_framework import serializers
from .models import Resturant


class ResturantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resturant
        fields = ("name", "location")
