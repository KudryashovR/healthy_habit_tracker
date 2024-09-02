from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.models import CustomUser
from main.permissions import IsOwnerOrReadOnly


class MockObject:
    """
    Класс-оболочка, имитирующий объект с полем владельца (owner).

    Атрибуты:
        owner : CustomUser
            Пользователь, который считается владельцем данного объекта.
    """

    def __init__(self, owner):
        self.owner = owner


class TestIsOwnerOrReadOnly(TestCase):
    """
    Тесты для проверки разрешений IsOwnerOrReadOnly.

    Данный класс тестов проверяет корректность работы пользовательского разрешения,
    которое должно позволять изменение объекта только его владельцу, а чтение — всем пользователям.

    Методы:
        setUp():
            Инициализация тестового окружения: фабрика запросов, объект разрешения
            и два тестовых пользователя для проверки разрешений.

        test_permission_allows_read_methods():
            Проверяет, что запросы методов чтения (GET, HEAD, OPTIONS) разрешены для не-владельцев объекта.

        test_permission_denies_write_methods_to_non_owner():
            Проверяет, что запросы методов записи (POST, PUT, PATCH, DELETE) отклоняются для не-владельцев объекта.

        test_permission_allows_write_methods_to_owner():
            Проверяет, что запросы методов записи (POST, PUT, PATCH, DELETE) разрешены владельцу объекта.
    """

    def setUp(self):
        """
        Инициализация тестового окружения.

        Создает фабрику запросов, экземпляр разрешения IsOwnerOrReadOnly и двух пользователей. Пользователь1 будет
        владельцем объекта, а пользователь2 используется для проверки доступа не-владельцев.
        """

        self.factory = APIRequestFactory()
        self.permission = IsOwnerOrReadOnly()
        self.user1 = CustomUser.objects.create_user(email='user1@example.com', tg_id=12345678, password='password')
        self.user2 = CustomUser.objects.create_user(email='user2@example.com', tg_id=23456789, password='password')
        self.obj = MockObject(owner=self.user1)

    def test_permission_allows_read_methods(self):
        """
        Тестирует, что разрешение позволяет методы чтения (GET, HEAD, OPTIONS) для всех пользователей.
        """

        for method in ['GET', 'HEAD', 'OPTIONS']:
            request = self.factory.generic(method, '/')
            request.user = self.user2
            self.assertTrue(self.permission.has_object_permission(request, None, self.obj))

    def test_permission_denies_write_methods_to_non_owner(self):
        """
        Тестирует, что разрешение запрещает методы записи (POST, PUT, PATCH, DELETE) для не-владельцев.
        """

        for method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            request = self.factory.generic(method, '/')
            request.user = self.user2
            self.assertFalse(self.permission.has_object_permission(request, None, self.obj))

    def test_permission_allows_write_methods_to_owner(self):
        """
        Тестирует, что разрешение позволяет методы записи (POST, PUT, PATCH, DELETE) владельцу объекта.
        """

        for method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            request = self.factory.generic(method, '/')
            request.user = self.user1
            self.assertTrue(self.permission.has_object_permission(request, None, self.obj))
