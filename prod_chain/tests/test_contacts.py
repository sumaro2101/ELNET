from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

from prod_chain.models import Contact


class TestContact(APITestCase):
    """Тесты контактов"""

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            "test",
            "test@gmail.com",
            "testproduct",
        )
        self.client.force_authenticate(user)
        self.url = "http://localhost/api/contacts/"

    def test_create_contact(self):
        """Тест создания контакта"""
        data = dict(name="test",
                    role="factory",
                    email='test@gmail.com',
                    country='RU',
                    town='Омск',
                    street='Ул.Химиков',
                    build='55Б',
                    )
        responce = self.client.post(self.url, data, format="json")

        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)

    def test_create_contact_permission_fail(self):
        """Тест создания контакта без прав доступа"""
        data = dict(name="test",
                    role="factory",
                    email='test@gmail.com',
                    country='RU',
                    town='Омск',
                    street='Ул.Химиков',
                    build='55Б',
                    )
        self.client.logout()
        responce = self.client.post(self.url, data, format="json")

        self.assertEqual(responce.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Contact.objects.count(), 0)

    def test_update_contact(self):
        """
        Тест обновления контакта
        """
        data = dict(name="test",
                    role="factory",
                    email='test@gmail.com',
                    country='RU',
                    town='Омск',
                    street='Ул.Химиков',
                    build='55Б',
                    )
        obj = Contact.objects.create(**data)

        data = dict(name="test_1")
        responce = self.client.patch(self.url + f"{obj.pk}/",
                                     data, format="json")
        product = Contact.objects.get(pk=obj.pk)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(product.name, "test_1")

    def test_update_contact_permission_fail(self):
        """
        Тест обновления контакта без прав доступа
        """
        data = dict(name="test",
                    role="factory",
                    email='test@gmail.com',
                    country='RU',
                    town='Омск',
                    street='Ул.Химиков',
                    build='55Б',
                    )
        obj = Contact.objects.create(**data)

        data = dict(name="test_1")
        self.client.logout()
        responce = self.client.patch(self.url + f"{obj.pk}/",
                                     data, format="json")
        product = Contact.objects.get(pk=obj.pk)
        self.assertEqual(responce.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(product.name, "test")

    def test_destroy_contact(self):
        """
        Тест удаление контакта
        """
        data = dict(name="test",
                    role="factory",
                    email='test@gmail.com',
                    country='RU',
                    town='Омск',
                    street='Ул.Химиков',
                    build='55Б',
                    )
        obj = Contact.objects.create(**data)

        responce = self.client.delete(self.url + f'{obj.pk}/')
        self.assertEqual(responce.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED,
                         )
        self.assertEqual(Contact.objects.count(), 1)
