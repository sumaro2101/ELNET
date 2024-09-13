from rest_framework import serializers

from django_countries.serializers import CountryFieldMixin

from . import models
from . import validators


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товара
    """

    class Meta:
        model = models.Product
        fields = '__all__'


class ContactSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """Сериализатор контактов
    """

    class Meta:
        model = models.Contact
        fields = '__all__'


class ProdMapSerializer(serializers.ModelSerializer):
    """Сериализатор цепочки
    """

    class Meta:
        model = models.ProdMap
        fields = '__all__'
        validators = [
            validators.RoleValidator('prod_object',
                                     'supplier',
                                     ),
            validators.DutyCheckValidator('duty'),
        ]


class ProdMapUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор цепочки
    """

    class Meta:
        model = models.ProdMap
        exclude = ('duty',)
        validators = [
            validators.RoleValidator('prod_object',
                                     'supplier',
                                     ),
        ]
