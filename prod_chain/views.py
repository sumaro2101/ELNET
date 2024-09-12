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


class ProdmapAPIViewser(CreateUpdateViewSet):
    """
    Енд поинт цепочки
    """
    queryset = models.ProdMap.objects.select_related('prod_object')

    def get_serializer_class(self):
        if self.action != 'update':
            return serializers.ProdMapSerializer
        return serializers.ProdMapUpdateSerializer 
