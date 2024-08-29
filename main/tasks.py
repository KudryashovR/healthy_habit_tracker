from celery import shared_task

from main.services import send_telegram_message


@shared_task
def send_tg_notification(action, chat_id, reward=None):
    """
    Отправляет уведомление в Telegram о выполнении задачи.

    Аргументы:
        action : str
            Название или описание действия, о выполнении которого необходимо напомнить.
        chat_id : int или str
            Идентификатор чата в Telegram, куда будет отправлено сообщение.
        reward : str, optional
            Награда, которую можно получить за выполнение задачи. Если не указано, сообщение будет без упоминания
            награды.

    Возвращает:
        None

    Описание:
        Формирует сообщение на основе переданных аргументов и отправляет его в указанный чат Telegram при помощи
        функции send_telegram_message.

    Задача:
        Выполняется как фоновая задача, используя декоратор @shared_task.
    """

    if reward:
        message = f"Напоминаю о выполнении задачи {action}. Выполнив эту задачу вы можете получить {reward}!"
    else:
        message = f"Напоминаю о выполнении задачи {action}."

    send_telegram_message(chat_id, message)
