from loguru import logger

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


class ProdmapAPIViewset(CreateUpdateViewSet):
    """
    Енд поинт цепочки
    """
    queryset = models.ProdMap.objects.select_related('prod_object')

    def get_serializer_class(self):
        logger.debug(f'{self.__class__.__name__} get action: {self.action}')
        if self.action != 'partial_update':
            logger.debug(f'{self.__class__.__name__} is return serializer: ProdMapSerializer')
            return serializers.ProdMapSerializer
        logger.debug(f'{self.__class__.__name__} is return serializer: ProdMapUpdateSerializer ')
        return serializers.ProdMapUpdateSerializer 
