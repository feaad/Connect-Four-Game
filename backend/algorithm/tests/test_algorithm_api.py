"""
File: test_algorithm_api.py
Project: Backend - Connect Four
File Created: Sunday, 21st July 2024 6:56:56 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Test the algorithm API.
-----
Last Modified: Sunday, 21st July 2024 9:42:00 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from algorithm.serializers import (
    AlgorithmDetailSerializer,
    AlgorithmSerializer,
)
from core.models import Algorithm
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITransactionTestCase

ALGO_URL = reverse("algorithm:algorithm-list")


def create_algorithm(
    name: str = "test_algorithm",
    description: str = "This is a test algorithm.",
) -> Algorithm:
    """
    Create and return a new algorithm.

    """

    return Algorithm.objects.create(name=name, description=description)


def detail_url(algo_algorithm_id: str) -> str:
    """
    Create and return a algorithm detail URL.

    """

    return reverse("algorithm:algorithm-detail", args=[algo_algorithm_id])


class PublicUserAPITests(APITransactionTestCase):
    """
    API Requests that do not require Authentication.

    """

    def setUp(self) -> None:
        """Initialize an instance of APIClient."""
        self.client = APIClient()

    def test_retrieve_algorithm(self) -> None:
        """
        Test retrieving a list of algorithm.

        """

        create_algorithm("test_1")
        create_algorithm("test_2")

        response = self.client.get(ALGO_URL)

        algorithm = Algorithm.objects.all().order_by("algorithm_id")
        serializer = AlgorithmSerializer(algorithm, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_get_algorithm_detail(self) -> None:
        """
        Test get details on an algorithm.

        """
        algo = create_algorithm()

        url = detail_url(algo.algorithm_id)
        response = self.client.get(url)

        serializer = AlgorithmDetailSerializer(algo)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
