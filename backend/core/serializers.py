"""
File: serializers.py
Project: Backend - Connect Four
File Created: Saturday, 20th July 2024 4:13:33 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Serializers for the core app.
-----
Last Modified: Saturday, 20th July 2024 4:18:23 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""


from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    """
    Serializer for the health check endpoint.

    """

    healthy = serializers.BooleanField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
