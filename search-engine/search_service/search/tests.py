from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Resturant
from .serializers import ResturantSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_resturant(name="", location=""):
        if name != "" and location != "":
            Resturant.objects.create(name=name, location=location)

    def setUp(self):
        # add test data
        self.create_resturant("Chipotle", "Hoboken,NJ")
        self.create_resturant("Karma cafe", "Hoboken,NJ")
        self.create_resturant("Sheraton", "Weehawken,NJ")


class GetAllResturantsTest(BaseViewTest):

    def test_get_all_resturants(self):
        """
        This test ensures that all resturants added in the setUp method
        exist when we make a GET request to the resturants/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("resturant-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Resturant.objects.all()
        serialized = ResturantSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
