from core.dataclasses import Status as cfs
from core.models import MatchMakingQueue, Player
from core.tests.helper import create_match_making, create_status, create_user
from django.urls import reverse
from game.serializers import MatchMakingQueueSerializer
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

REQUEST_URL = reverse("game:match:match-request")
CANCEL_URL = reverse("game:match:match-cancel")
MATCH_URL = reverse("game:match-list")


class PrivateUserAPITests(APITestCase):
    """
    API Requests that do require Authentication

    """

    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.queued_status = create_status(
            cfs.QUEUED.value, "The player is in the queue."
        )
        self.cancelled_status = create_status(
            cfs.CANCELLED.value, "The player has cancelled the match."
        )
        self.matched_status = create_status(
            cfs.MATCHED.value, "The player has been matched."
        )

    def test_request_match(self) -> None:
        """
        Test creating a new match making queue.

        """

        response = self.client.post(REQUEST_URL)

        match_making_queue = MatchMakingQueue.objects.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MatchMakingQueue.objects.count(), 1)
        self.assertEqual(
            response.data["status"], "Player added to matchmaking queue"
        )
        self.assertEqual(
            response.data["queue_id"], str(match_making_queue.first().queue_id)
        )

    def test_request_match_twice(self) -> None:
        """
        Test creating a new match making queue twice.

        """

        self.client.post(REQUEST_URL)
        response = self.client.post(REQUEST_URL)
        match_making_queue = MatchMakingQueue.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["status"], "Player already in matchmaking queue"
        )
        self.assertEqual(
            response.data["queue_id"], str(match_making_queue.first().queue_id)
        )

    def test_cancel_match(self) -> None:
        """
        Test cancelling a match making queue.

        """

        self.client.post(REQUEST_URL)

        response = self.client.post(CANCEL_URL)
        match_making_queue = MatchMakingQueue.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Match making cancelled")
        self.assertEqual(match_making_queue.first().status.name, "Cancelled")

    def test_cancel_match_no_queue(self) -> None:
        """
        Test cancelling a match making queue that does not exist.

        """

        response = self.client.post(CANCEL_URL)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "Match making not found")

    def test_cancel_match_when_matched(self) -> None:
        """
        Test cancelling a match making queue that has been matched.

        """

        self.client.post(REQUEST_URL)

        match_making_queue = MatchMakingQueue.objects.all().first()
        match_making_queue.status = self.matched_status
        match_making_queue.save()

        response = self.client.post(CANCEL_URL)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "Match making not found")

    def test_return_matches(self) -> None:
        """
        Test returning matches making queue.

        """

        create_match_making()
        MatchMakingQueue.objects.create(
            player=Player.objects.get(user=self.user),
            status=self.queued_status,
        )
        MatchMakingQueue.objects.create(
            player=Player.objects.get(user=self.user),
            status=self.cancelled_status,
        )
        MatchMakingQueue.objects.create(
            player=Player.objects.get(user=self.user),
            status=self.matched_status,
        )

        response = self.client.get(MATCH_URL)

        matches = (
            MatchMakingQueue.objects.all()
            .filter(player__user=self.user)
            .order_by("created_at")
        )

        serializer = MatchMakingQueueSerializer(matches, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 3)

    def test_return_matches_no_matches(self) -> None:
        """
        Test returning matches making queue with no matches that belong to the
        user.

        """

        create_match_making()
        response = self.client.get(MATCH_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_return_match(self) -> None:
        """
        Test returning a match making queue.

        """

        match = MatchMakingQueue.objects.create(
            player=Player.objects.get(user=self.user),
            status=self.matched_status,
        )

        response = self.client.get(
            reverse("game:match-detail", args=[match.queue_id])
        )

        serializer = MatchMakingQueueSerializer(match)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
