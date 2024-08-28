from rest_framework import generics

from main.models import Habit
from main.serializers import HabitSerializer


class HabitListCreate(generics.ListCreateAPIView):
    """
    Представление для списка и создания объектов Habit.

    Данный класс позволяет получать список всех объектов Habit, а также создавать новые объекты Habit.

    Атрибуты:
        queryset (QuerySet): Все объекты модели Habit.
        serializer_class (Serializer): Класс сериализатора, который будет использован для сериализации и десериализации
                                       данных.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления объекта Habit по его идентификатору.

    Данный класс позволяет выполнять операции получения, обновления и удаления конкретного объекта Habit.

    Атрибуты:
        queryset (QuerySet): Все объекты модели Habit.
        serializer_class (Serializer): Класс сериализатора, который будет использован для сериализации и десериализации
                                       данных.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
