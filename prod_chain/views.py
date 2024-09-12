from rest_framework import generics, viewsets

from .viewsets import CreateUpdateViewSet
from . import models, serializers


class ProductAPIView(CreateUpdateViewSet):
    """Создание товара
    """
    queryset = models.Product.objects.get_queryset()
    serializer_class = serializers.ProductSerializer
