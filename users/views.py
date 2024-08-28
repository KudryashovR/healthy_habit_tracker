from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import CustomUser
from users.serializers import UserProfileSerializer


class UserCreate(generics.CreateAPIView):
    """
    Класс представления для создания нового пользователя.

    Атрибуты:
        queryset (QuerySet): Набор запросов для модели CustomUser.
        serializer_class (Serializer): Класс сериализатора, используемый для валидации и десериализации входных данных.
        permission_classes (list): Список классов разрешений, применяемых к этому представлению. В данном случае
                                   разрешен доступ для всех.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
