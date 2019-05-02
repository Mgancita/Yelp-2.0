from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Resturant
from .serializers import ResturantSerializer

    

class ListResturantView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Resturant.objects.all()
    serializer_class = ResturantSerializer
