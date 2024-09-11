from rest_framework import generics, viewsets

from . import models, serializers


class CreateProductAPIView(viewsets.ModelViewSet):
    """Создание товара
    """
    queryset = models.Product
    serializer_class = serializers.ProductSerializer
