from datetime import date

from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

from prod_chain.models import Product


class TestProduct(APITestCase):
    """Тесты товара"""

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            "test",
            "test@gmail.com",
            "testproduct",
        )
        self.client.force_authenticate(user)
        self.url = "http://localhost/api/products/"

    def test_create_product(self):
        """Тест создания продукта"""
        data = dict(name="test", model="test_model", realize=date.today())
        responce = self.client.post(self.url, data, format="json")

        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_permission_fail(self):
        """Тест создания продукта без прав доступа"""
        data = dict(name="test", model="test_model", realize=date.today())
        self.client.logout()
        responce = self.client.post(self.url, data, format="json")

        self.assertEqual(responce.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), 0)

    def test_update_product(self):
        """
        Тест обновления продукта
        """
        data = dict(name="test", model="test_model", realize=date.today())
        obj = Product.objects.create(**data)

        data = dict(name="test_1", model="test_model_1")
        responce = self.client.patch(self.url + f"{obj.pk}/",
                                     data, format="json")
        product = Product.objects.get(pk=obj.pk)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.name, "test_1")

    def test_update_product_permission_fail(self):
        """
        Тест обновления продукта без прав доступа
        """
        data = dict(name="test", model="test_model", realize=date.today())
        obj = Product.objects.create(**data)

        data = dict(name="test_1", model="test_model_1")
        self.client.logout()
        responce = self.client.patch(self.url + f"{obj.pk}/",
                                     data, format="json")
        product = Product.objects.get(pk=obj.pk)
        self.assertEqual(responce.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(product.name, "test")

    def test_destroy_product(self):
        """
        Тест удаление продукта
        """
        data = dict(name="test", model="test_model", realize=date.today())
        obj = Product.objects.create(**data)

        responce = self.client.delete(self.url + f'{obj.pk}/')
        self.assertEqual(responce.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED,
                         )
        self.assertEqual(Product.objects.count(), 1)
