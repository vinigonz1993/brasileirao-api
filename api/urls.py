from django.urls import include, path

from rest_framework import routers

from api.viewsets import (
    RoundsViewSet, TeamsViewSet, SeasonsViewSet
)

router = routers.DefaultRouter()

router.register(
    'teams',
    TeamsViewSet,
    basename='Usuario'
)

urlpatterns = [
    path(
        'teams/',
        TeamsViewSet.as_view()
    ),
    path(
        'seasons/',
        SeasonsViewSet.as_view()
    ),
    path(
        'rounds/',
        RoundsViewSet.as_view()
    )
]