from django.test import TestCase
from django.core.exceptions import ValidationError
from main.models import Habit
from users.models import CustomUser
import datetime


class HabitModelTest(TestCase):
    """
    Создаем пользователя с необходимыми полями
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@test.ts',
            password='testpassword',
            tg_id='123456789'
        )

    def test_create_valid_habit(self):
        """
        Тест валидной привычки
        """

        habit = Habit.objects.create(
            owner=self.user,
            place='Home',
            time=datetime.time(10, 0),
            action='Read Book',
            is_pleasant_habit=True,
            frequency=3,
            time_to_complete=90,
            is_public=True
        )

        self.assertEqual(habit.owner, self.user)
        self.assertEqual(habit.action, 'Read Book')

    def test_invalid_frequency(self):
        """
        Проверка на частоту больше 7
        """

        habit = Habit(
            owner=self.user,
            place='Office',
            time=datetime.time(15, 0),
            action='Exercise',
            frequency=10,
            time_to_complete=60,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_invalid_time_to_complete(self):
        """
        Проверка на время выполнения больше 120 секунд
        """

        habit = Habit(
            owner=self.user,
            place='Gym',
            time=datetime.time(8, 0),
            action='Workout',
            frequency=2,
            time_to_complete=130,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_related_habit_and_reward(self):
        """
        Проверка на одновременное указание связанной привычки и награды
        """

        related_habit = Habit.objects.create(
            owner=self.user,
            place='Park',
            time=datetime.time(7, 0),
            action='Running',
            frequency=1,
            time_to_complete=45,
            is_pleasant_habit=False
        )

        habit = Habit(
            owner=self.user,
            place='Home',
            time=datetime.time(9, 0),
            action='Meditate',
            related_habit=related_habit,
            reward='Ice Cream',
            frequency=3,
            time_to_complete=30
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_pleasant_habit_constraints(self):
        """
        Приятная привычка не может иметь связанную привычку или награду
        """

        related_habit = Habit.objects.create(
            owner=self.user,
            place='Park',
            time=datetime.time(7, 0),
            action='Running',
            frequency=1,
            time_to_complete=45,
            is_pleasant_habit=False
        )

        habit = Habit(
            owner=self.user,
            place='Home',
            time=datetime.time(9, 0),
            action='Yoga',
            is_pleasant_habit=True,
            related_habit=related_habit,
            reward='Chocolate',
            frequency=2,
            time_to_complete=50
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_str_method(self):
        """
        Проверка на корректность работы метода __str__()
        """

        habit = Habit.objects.create(
            owner=self.user,
            place='Library',
            time=datetime.time(12, 0),
            action='Study',
            is_pleasant_habit=True,
            frequency=4,
            time_to_complete=60,
            is_public=False
        )
        self.assertEqual(str(habit), 'Study')
