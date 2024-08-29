import json
from datetime import datetime

from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from main.models import Habit


@receiver(post_save, sender=Habit)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    """
    Создает или обновляет периодическую задачу для отправки уведомлений в Telegram после сохранения объекта Habit.

    Аргументы:
        sender : модель
            Модель, пославшая сигнал (в данном случае Habit).
        instance : Habit
            Экземпляр модели Habit, который был сохранен.
        created : bool
            Флаг, указывающий, был ли создан новый объект Habit (True) или обновлен существующий (False).
        **kwargs : dict
            Дополнительные аргументы.

    Описание:
        Создается или находится существующая запись в таблице IntervalSchedule с интервалом, соответствующим
        указанной пользователем периодичности привычки. Затем создается или обновляется запись в таблице PeriodicTask,
        которая настроена на отправку уведомлений в Telegram. Уведомление включает в себя действие,
        идентификатор чата в Telegram и награду, связанные с этой привычкой.

    Возвращает:
        None
    """

    schedule, created_schedule = IntervalSchedule.objects.get_or_create(
        every=instance.frequency,
        period=IntervalSchedule.DAYS,
    )

    task_name = f"notification_{instance.action}_for_user_{instance.owner}"
    task, created_task = PeriodicTask.objects.update_or_create(
        name=task_name,
        defaults={
            "interval": schedule,
            "task": "main.tasks.send_tg_notification",
            "start_time": timezone.make_aware(
                datetime.combine(datetime.now().date(), instance.time)
            ),
            "kwargs": json.dumps(
                {
                    "action": instance.action,
                    "chat_id": instance.owner.tg_id,
                    "reward": instance.reward,
                }
            ),
        },
    )

    if not created_task:
        task.interval = schedule
        task.save()


@receiver(post_delete, sender=Habit)
def delete_periodic_task(sender, instance, **kwargs):
    """
    Удаляет периодическую задачу для отправки уведомлений в Telegram после удаления объекта Habit.

    Аргументы:
        sender : модель
            Модель, пославшая сигнал (в данном случае Habit).
        instance : Habit
            Экземпляр модели Habit, который был удален.
        **kwargs : dict
            Дополнительные аргументы.

    Описание:
        Удаляет запись из таблицы PeriodicTask, связанной с удаленной привычкой на основе ее действия и владельца.

    Возвращает:
        None
    """

    task_name = f"notification_{instance.action}_for_user_{instance.owner}"
    PeriodicTask.objects.filter(name=task_name).delete()
