from datetime import date

from django.test import TestCase
from rest_framework.validators import ValidationError

from prod_chain.models import (ProdMap,
                               Product,
                               Contact,
                               )
from prod_chain.validators import (ProductListValidator,
                                   DutyCheckValidator,
                                   RoleValidator,
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
                     products=[self.product_1])
        validator = ProductListValidator('products', 'supplier')
        
        self.assertIsNone(validator(attrs, self.serializer))

    def test_validator_products_fail(self):
        """
        Тест провальной валидации
        """
        product_3 = Product.objects.create(**dict(name="test_3",
                                                  model="test_model_3",
                                                  realize=date.today(),
                                                  ))
        attrs = dict(supplier=self.net_chain,
                     products=[self.product_1, self.product_2, product_3])
        validator = ProductListValidator('products', 'supplier')

        with self.assertRaises(ValidationError):
            validator(attrs, self.serializer)

    def test_validator_duty_validator(self):
        """
        Тест валидатора на долг
        """
        attrs = dict(duty=10.00)
        validator = DutyCheckValidator('duty')
        
        self.assertIsNone(validator(attrs))

    def test_validator_duty_validator_fail(self):
        """
        Тест провальной валидации
        """
        attrs = dict(duty=-33.00)
        validator = DutyCheckValidator('duty')
        
        with self.assertRaises(ValidationError):
            validator(attrs)

    def test_validator_role(self):
        """
        Тест валидатора роли
        """
        contact = Contact.objects.create(
            **dict(name="test_1",
                    role="retail",
                    email='test_1@gmail.com',
                    country='RU',
                    town='Омск',
                    street='Ул.Химиков',
                    build='55Б',
                    )
        )
        attrs = dict(prod_object=contact,
                     supplier=self.net_chain,
                    )
        validator = RoleValidator('prod_object',
                                  'supplier')
        self.assertIsNone(validator(attrs, self.serializer))

    def test_validator_role(self):
        """
        Тест провальной валидации
        """
        contact = Contact.objects.create(
            **dict(name="test_1",
                    role="retail",
                    email='test_1@gmail.com',
                    country='RU',
                    town='Омск',
                    street='Ул.Химиков',
                    build='55Б',
                    )
        )
        net_chain = ProdMap.objects.create(
            **dict(
                prod_object=contact,
                supplier=self.net_chain,
                duty=0,
            ),
        )
        net_chain.products.add(self.product_1)
        net_chain.products.add(self.product_2)
        prod_object = Contact.objects.create(
            **dict(name="test_2",
                    role="factory",
                    email='test_1@gmail.com',
                    country='RU',
                    town='Омск',
                    street='Ул.Химиков',
                    build='55Б',
                    )
        )
        attrs = dict(prod_object=prod_object,
                     supplier=net_chain,
                    )
        validator = RoleValidator('prod_object',
                                  'supplier')
        with self.assertRaises(ValidationError):
            validator(attrs, self.serializer)
