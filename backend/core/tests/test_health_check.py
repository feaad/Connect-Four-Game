"""
File: test_health_check.py
Project: Backend - Connect Four
File Created: Thursday, 18th July 2024 6:09:14 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Test health check.
-----
Last Modified: Thursday, 18th July 2024 6:09:36 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class HealthCheckTests(TestCase):
    """Test health check."""

    def test_health_check(self):
        """
        Unit Test for health check.

        """
        client = APIClient()
        url = reverse("core:health-check")
        res = client.get(url)

        self.assertEqual(res.data, {"healthy": True})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
