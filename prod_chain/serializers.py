from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товара
    """

    class Meta:
        model = models.Product
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
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


class ProdMapUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор цепочки
    """

    class Meta:
        model = models.ProdMap
        exclude = ('duty',)
