from django.urls import path
from .views import ListResturantView


urlpatterns = [
    path('resturants/', ListResturantView.as_view(), name="resturant-all")
]

