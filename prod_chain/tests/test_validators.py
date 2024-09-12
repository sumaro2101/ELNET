from datetime import date

from loguru import logger

from django.test import TestCase
from rest_framework.validators import ValidationError

from prod_chain.models import (ProdMap,
                               Product,
                               Contact,
                               )
from prod_chain.validators import (ProductListValidator,
                                   )


class TestValidators(TestCase):
    """
    Тесты валидатора
    """
    def setUp(self) -> None:
        contact = Contact.objects.create(
            **dict(name="test",
                    role="factory",
                    email='test@gmail.com',
                    country='RU',
                    town='Омск',
                    street='Ул.Химиков',
                    build='55Б',
                    )
        )
        self.product_1 = Product.objects.create(**dict(name="test_1",
                                                  model="test_model_1",
                                                  realize=date.today(),
                                                  ))
        self.product_2 = Product.objects.create(**dict(name="test_2",
                                                  model="test_model_2",
                                                  realize=date.today(),
                                                  ))
        self.net_chain = ProdMap.objects.create(
            **dict(
                prod_object=contact,
                supplier=None,
                duty=0,
            ),
        )
        self.net_chain.products.add(self.product_1)
        self.net_chain.products.add(self.product_2)

        class Serializer:
            class Instance:
                supplier = self.net_chain
            instance = Instance

        self.serializer = Serializer

    def test_validator_product_correct(self):
        """
        Тест валидатора на проверку продуктов
        """
        attrs = dict(supplier=self.net_chain,
                     products=[self.product_1.pk])
        validator = ProductListValidator('products', 'supplier')
        
        self.assertIsNone(validator(attrs, self.serializer))

    def test_validator_products_fail(self):
        """
        Тест провальной валидации
        """
        attrs = dict(supplier=self.net_chain,
                     products=[self.product_1.pk, self.product_2.pk, 44])
        validator = ProductListValidator('products', 'supplier')

        with self.assertRaises(ValidationError):
            validator(attrs, self.serializer)
