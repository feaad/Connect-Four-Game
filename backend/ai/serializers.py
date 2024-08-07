"""
File: serializers.py
Project: Backend - Connect Four
File Created: Sunday, 21st July 2024 6:54:45 PM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: Serializers for the Algorithm model.
-----
Last Modified: Sunday, 21st July 2024 7:17:35 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from core.models import Algorithm
from rest_framework import serializers


class AlgorithmSerializer(serializers.ModelSerializer):
    """
    Serializer for the Algorithm model.
    """

    class Meta:
        """
        Meta class for the AlgorithmSerializer

        """

        model = Algorithm
        fields = ["algorithm_id", "name", "code_name"]
        read_only_fields = ["algorithm_id"]


class AlgorithmDetailSerializer(AlgorithmSerializer):
    """
    Serializer for recipe detail view.
    """

    class Meta(AlgorithmSerializer.Meta):
        """
        Meta class for the AlgorithmDetailSerializer

        """

        fields = AlgorithmSerializer.Meta.fields + ["description", "depth"]
