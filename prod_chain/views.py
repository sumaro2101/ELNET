from loguru import logger

from django_filters.rest_framework import backends as filters

from .viewsets import CreateUpdateViewSet
from . import models, serializers


class ProductAPIViewset(CreateUpdateViewSet):
    """
    Енд поинт товара
    """
    queryset = models.Product.objects.get_queryset()
    serializer_class = serializers.ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ('name',
                        'model',
                        'realize',
                        )


class ContactAPIViewset(CreateUpdateViewSet):
    """
    Енд поинт контактов
    """
    queryset = models.Contact.objects.get_queryset()
    serializer_class = serializers.ContactSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ('name',
                        'role',
                        'email',
                        'country',
                        'town',
                        'street',
                        'build',
                        )


class ProdmapAPIViewset(CreateUpdateViewSet):
    """
    Енд поинт цепочки
    """
    queryset = models.ProdMap.objects.select_related('prod_object')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ('prod_object',
                        'products',
                        'supplier',
                        'duty',
                        'appoiment_date',
                        )

    def get_serializer_class(self):
        logger.debug(f'{self.__class__.__name__} get action: {self.action}')
        if self.action == 'partial_update':
            logger.debug(f'{self.__class__.__name__} is return serializer: ProdMapUpdateSerializer')
            return serializers.ProdMapUpdateSerializer
        if self.action == 'create':
            logger.debug(f'{self.__class__.__name__} is return serializer: ProdMapCreateSerializer')
            return serializers.ProdMapCreateSerializer
        logger.debug(f'{self.__class__.__name__} is return serializer: ProdMapSerializer')
        return serializers.ProdMapSerializer

    def get_queryset(self):
        prod_map = models.ProdMap.objects.get_queryset()
        query_params = self.request.query_params
        if country := query_params.get('country'):
            logger.debug(f'query_params get country with value {country}')
            prod_map = prod_map.filter(prod_object__country=country)
        if role := query_params.get('role'):
            logger.debug(f'query_params get role with value {role}')
            prod_map = prod_map.filter(prod_object__role=role)
        return prod_map
