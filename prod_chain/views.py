from rest_framework import generics, viewsets

from .viewsets import CreateUpdateViewSet
from . import models, serializers


class ProductAPIViewset(CreateUpdateViewSet):
    """
    Енд поинт товара
    """
    queryset = models.Product.objects.get_queryset()
    serializer_class = serializers.ProductSerializer


class ContactAPIViewset(CreateUpdateViewSet):
    """
    Енд поинт контактов
    """
    queryset = models.Contact.objects.get_queryset()
    serializer_class = serializers.ContactSerializer
