from rest_framework import serializers

from main.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit.

    Данный класс определяет, какие поля модели Habit будут сериализоваться и десериализоваться.

    Вложенный класс Meta:
        model (Model): Модель, которую нужно сериализовать.
        fields (str): Поля, которые нужно включить в сериализацию.
    """

    class Meta:
        model = Habit
        fields = '__all__'
