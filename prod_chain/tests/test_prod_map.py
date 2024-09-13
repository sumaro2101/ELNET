from datetime import date

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from prod_chain.models import Contact, Product, ProdMap


class TestProdMap(APITestCase):
    """
    Тест цепочки
    """
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            "test",
            "test@gmail.com",
            "testproduct",
        )
        self.client.force_authenticate(user)
        self.contact = Contact.objects.create(
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
        self.url = "http://localhost/api/prod-map/"

    def test_create_prod_map(self):
        """
        Тест создания цепочки
        """
        data = dict(
                prod_object=self.contact.pk,
                products=[self.product_1.pk, self.product_2.pk],
                supplier=None,
                duty=0,
                )
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProdMap.objects.count(), 1)

    def test_update_prod_map(self):
        """
        Тест обновления цепочки
        """
        net_chain = ProdMap.objects.create(
            **dict(
                prod_object=self.contact,
                supplier=None,
                duty=0,
            ),
        )
        net_chain.products.add(self.product_1)
        net_chain.products.add(self.product_2)
        data = dict(products=[self.product_2.pk,])
        response = self.client.patch(self.url + f'{net_chain.pk}/',
                                    data,
                                    format='json',
                                    )
        products = ProdMap.objects.get(pk=net_chain.pk).products.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(products, 1)

    def test_update_duty_now_allowed(self):
        """
        Тест не поддержания обновления долга
        """
        net_chain = ProdMap.objects.create(
            **dict(
                prod_object=self.contact,
                supplier=None,
                duty=0,
            ),
        )
        net_chain.products.add(self.product_1)
        net_chain.products.add(self.product_2)
        data = dict(duty=123.22)
        self.client.patch(self.url + f'{net_chain.pk}/',
                                    data,
                                    format='json',
                                    )
        duty = ProdMap.objects.get(pk=net_chain.pk).duty
        self.assertEqual(duty, 0)

    def test_delete_prod_fail(self):
        """
        Тест не возможности удаления цепочки
        """
        net_chain = ProdMap.objects.create(
            **dict(
                prod_object=self.contact,
                supplier=None,
                duty=0,
            ),
        )
        net_chain.products.add(self.product_1)
        net_chain.products.add(self.product_2)
        response = self.client.delete(self.url + f'{net_chain.pk}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(ProdMap.objects.count(), 1)
