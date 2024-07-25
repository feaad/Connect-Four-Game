from core.models import MatchMakingQueue
from core.tests.helper import create_user
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from game.serializers import MatchMakingQueueSerializer

REQUEST_URL = reverse("game:match:match-request")


class PrivateUserAPITests(APITestCase):
    """
    API Requests that do require Authentication

    """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_request_match(self):
        """
        Test creating a new match making queue.

        """

        response = self.client.post(REQUEST_URL)

        match_making_queue = MatchMakingQueue.objects.all()
        serializer = MatchMakingQueueSerializer(match_making_queue[0])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MatchMakingQueue.objects.count(), 1)
        self.assertEqual(response.data, serializer.data)

    def test_request_match_with_invalid_turn_preference(self):
        """
        Test creating a new match making queue with invalid turn preference.

        """

        response = self.client.post(
            REQUEST_URL, {"turn_preference": "invalid"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Invalid turn preference"})
