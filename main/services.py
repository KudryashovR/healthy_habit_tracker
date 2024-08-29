import requests

from config import settings


def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение в Telegram.

    Аргументы:
        chat_id : int или str
            Идентификатор чата в Telegram, куда будет отправлено сообщение.
        message : str
            Текст сообщения, которое будет отправлено.

    Возвращает:
        None

    Использует:
        requests.get для отправки HTTP-запроса на Telegram API.
    """

    params = {
        "chat_id": chat_id,
        "text": message,
    }

    requests.get(
        f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage", params=params
    )
