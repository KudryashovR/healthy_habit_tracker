from unittest import TestCase
from unittest.mock import patch
from main.tasks import send_tg_notification


class SendNotificationTests(TestCase):
    @patch('main.tasks.send_telegram_message')
    def test_send_notification_with_reward(self, mock_send_message):
        action = "drink_water"
        chat_id = 123456
        reward = "gold star"

        send_tg_notification(action, chat_id, reward)

        expected_message = (f"Напоминаю о выполнении задачи {action} через 15 минут. Выполнив эту задачу вы можете "
                            f"получить {reward}!")
        mock_send_message.assert_called_once_with(chat_id, expected_message)

    @patch('main.tasks.send_telegram_message')
    def test_send_notification_without_reward(self, mock_send_message):
        action = "drink_water"
        chat_id = 123456

        send_tg_notification(action, chat_id)

        expected_message = f"Напоминаю о выполнении задачи {action} через 15 минут."
        mock_send_message.assert_called_once_with(chat_id, expected_message)
