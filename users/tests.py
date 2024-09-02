from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserManagerTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = "testuser@example.com"
        password = "Testpass123"
        tg_id = 12345678
        user = User.objects.create_user(email=email, password=password, tg_id=tg_id)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_no_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="testpass")

    def test_create_superuser_with_email_and_tg_id_successful(self):
        email = "superuser@example.com"
        password = "Superpass123"
        tg_id = 123456789

        user = User.objects.create_superuser(email=email, tg_id=tg_id, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.tg_id, tg_id)

    def test_create_superuser_no_tg_id_raises_error(self):
        email = "superuser@example.com"
        password = "Superpass123"

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=email, tg_id=None, password=password)

    def test_create_superuser_is_staff_error(self):
        email = "superuser@example.com"
        password = "Superpass123"
        tg_id = 123456789

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=email, tg_id=tg_id, password=password, is_staff=False)

    def test_create_superuser_is_superuser_error(self):
        email = "superuser@example.com"
        password = "Superpass123"
        tg_id = 123456789

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=email, tg_id=tg_id, password=password, is_superuser=False)
