"""
File: router.py
Project: Backend - Connect Four
File Created: Sunday, 21st July 2024 12:12:11 AM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: A custom router for the system.
-----
Last Modified: Sunday, 21st July 2024 7:36:42 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from rest_framework.routers import DynamicRoute, Route, SimpleRouter


class CustomRouter(SimpleRouter):
    """
    A custom router
    """

    routes = [
        Route(
            url=r"^{prefix}/{lookup}$",
            mapping={
                "get": "retrieve",
                "patch": "partial_update",
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Detail"},
        ),
        Route(
            url=r"^{prefix}$",
            mapping={
                "post": "create",
            },
            name="{basename}-create",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        DynamicRoute(
            url=r"^{prefix}/{lookup}/{url_path}$",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={},
        ),
    ]
