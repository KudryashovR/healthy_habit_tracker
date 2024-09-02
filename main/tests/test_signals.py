from django.test import TestCase
from datetime import time
from django_celery_beat.models import PeriodicTask
from main.models import Habit
from users.models import CustomUser


class HabitSignalTests(TestCase):
    """
    Тесты для проверки сигналов, связанных с моделью Habit.

    Этот класс тестирует автоматическое создание, обновление и удаление периодических задач
    (PeriodicTask) при создании, обновлении и удалении привычек (Habit).

    Методы:
        setUp():
            Настроить тестовое окружение, создавая пользователя и данные привычки для использования в тестах.

        test_create_periodic_task_on_habit_creation():
            Проверяет, что при создании привычки создается соответствующая периодическая задача.

        test_update_periodic_task_on_habit_update():
            Проверяет, что обновление привычки приводит к обновлению соответствующей периодической задачи.

        test_delete_periodic_task_on_habit_deletion():
            Проверяет, что удаление привычки приводит к удалению соответствующей периодической задачи.
    """

    def setUp(self):
        """
        Инициализация тестового окружения.

        Создает тестового пользователя и словарь с данными привычки, которые будут использоваться в различных тестовых
        методах.
        """

        self.user = CustomUser.objects.create_user(email='user@example.com', tg_id=12345678, password='password')
        self.habit_data = {
            'owner': self.user,
            'action': 'drink_water',
            'frequency': 1,
            'time': time(8, 0),
            'reward': 'gold star',
            'time_to_complete': 60
        }

    def test_create_periodic_task_on_habit_creation(self):
        """
        Тестирует создание периодической задачи при создании привычки.
        """

        habit = Habit.objects.create(**self.habit_data)

        task_name = f"notification_{habit.action}_for_user_{habit.owner}"
        task_exists = PeriodicTask.objects.filter(name=task_name).exists()
        self.assertTrue(task_exists)

    def test_update_periodic_task_on_habit_update(self):
        """
        Тестирует обновление периодической задачи при обновлении привычки.
        """

        habit = Habit.objects.create(**self.habit_data)

        habit.frequency = 2
        habit.save()

        task_name = f"notification_{habit.action}_for_user_{habit.owner}"
        task = PeriodicTask.objects.get(name=task_name)
        self.assertEqual(task.interval.every, habit.frequency)

    def test_delete_periodic_task_on_habit_deletion(self):
        """
        Тестирует удаление периодической задачи при удалении привычки.
        """

        habit = Habit.objects.create(**self.habit_data)

        habit.delete()

        task_name = f"notification_{habit.action}_for_user_{habit.owner}"
        task_exists = PeriodicTask.objects.filter(name=task_name).exists()
        self.assertFalse(task_exists)
