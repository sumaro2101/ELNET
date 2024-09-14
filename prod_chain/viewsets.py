from rest_framework.mixins import (CreateModelMixin,
                                   UpdateModelMixin,
                                   RetrieveModelMixin,
                                   ListModelMixin,
                                   )
from rest_framework.viewsets import GenericViewSet


class CreateUpdateViewSet(CreateModelMixin,
                          UpdateModelMixin,
                          RetrieveModelMixin,
                          ListModelMixin,
                          GenericViewSet,
                          ):
    """
    Кастомный виювсет на создание и обновеление модели.
    """
    pass
