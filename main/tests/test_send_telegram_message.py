import unittest
from unittest.mock import patch

from config import settings
from main.services import send_telegram_message


class TestGramMessage(unittest.TestCase):
    """
    Тест отправки сообщений Telegram с помощью функции send_telegram_message.
    """

    @patch('requests.get')
    def test_gram_message(self, mock_get):
        mock_get.return_value.status_code = 200

        chat_id = 123456789
        message = "Hello, World!"

        send_telegram_message(chat_id, message)

        mock_get.assert_called_once_with(
            f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage",
            params={"chat_id": chat_id, "text": message}
        )
