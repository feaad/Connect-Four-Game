from ai.serializers import AlgorithmDetailSerializer, AlgorithmSerializer
from core.constants import BACKENDS
from core.models import Algorithm
from rest_framework import viewsets


class AlgorithmViewSet(viewsets.ModelViewSet):
    """
    View for algorithm APIs.
    """

    serializer_class = AlgorithmDetailSerializer
    queryset = Algorithm.objects.all()
    http_method_names = ["get"]
    authentication_classes = []

    filter_backends = BACKENDS
    filterset_fields = [
        "algorithm_id",
        "name",
        "code_name",
        "description",
        "depth",
    ]
    search_fields = [
        "algorithm_id",
        "name",
        "code_name",
        "description",
        "depth",
    ]
    ordering_fields = filterset_fields

    def get_queryset(self):
        """
        Retrieve all algorithms.

        """
        return self.queryset.order_by("algorithm_id")

    def get_serializer_class(self):
        """
        Return the serializer class for request.

        """
        return (
            AlgorithmSerializer
            if self.action == "list"
            else self.serializer_class
        )

    def perform_create(self, serializer):
        """
        Create a new algorithm.

        """
        serializer.save()
