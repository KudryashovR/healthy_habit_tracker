# healthy_habit_tracker

Бэкенд-часть SPA веб-приложения.

Трекер полезных привычек. Приложение помогает приобретению новых полезных привычек и искоренению старых плохих привычек.

## Технологический стек

Проект основан на следующих технологиях:

- Язык программирования: Python 3.12
- Веб-фреймворк: Django 5.1
  - Используется для построения веб-приложения и API.
- Базы данных: PostgreSQL (с использованием psycopg2-binary для подключения)
  - Для хранения данных приложения.
- Обработка изображений: Pillow 10.4.0
  - Для работы с изображениями, если это требуется функционалом приложения.
- Конфигурация окружения: django-environ 0.11.2
  - Для управления переменными окружения.
- REST API: Django REST Framework 3.15.2
  - Для создания RESTful API.
  - Аутентификация: djangorestframework-simplejwt 5.3.1
    - Для работы с JWT токенами в API.
- Документация API: drf-yasg 1.21.7
  - Для автоматической генерации документации API в формате Swagger.
- Очереди задач: Celery 5.4.0
  - Для асинхронного выполнения задач.
  - Планировщик задач: django-celery-beat 2.7.0
    - Для планирования периодических задач.
- Кэширование и брокер сообщений: Redis 5.0.8
  - Используется в качестве брокера для Celery и/или как средство кэширования.
- Интеграция с Telegram: python-telegram-bot 21.4
  - Для взаимодействия с Telegram через бот API.
- HTTP-запросы: requests 2.32.3
  - Для выполнения HTTP-запросов к внешним API.
- CORS: django-cors-headers 4.4.0
  - Для обработки CORS (Cross-Origin Resource Sharing) запросов.

### Инструменты для разработки и проверки кода

- Интерактивная оболочка: IPython 8.26.0
  - Для улучшенной интерактивности при работе в консоли.
- Тестирование покрытия кода: Coverage 7.6.1
  - Для оценки покрытия тестами.
- Форматирование кода: Black 24.8.0
  - Для автоматического форматирования кода.
- Линтер: Flake8 7.1.1
  - Для проверки качества и стиля кода.

## Установка и настройка

### Предварительные требования

- Python 3.12
- Установленный Poetry (или другой менеджер зависимостей)

### Установка

1. Клонируйте репозиторий

```bash
   git clone https://github.com/ваш-профиль/название-репозитория.git
   cd название-репозитория
```

2. Установите зависимости

```bash
   poetry install
```

3. Настройте переменные окружения

   Создайте файл .env в корне проекта и добавьте необходимые переменные окружения согласно файла `.env.example`

### Миграции базы данных

Выполните миграции для настройки базы данных:

```bash
poetry run python manage.py migrate
```

### Запуск сервера разработки

Запустите сервер разработки:

```bash
poetry run python manage.py runserver
```

## Тестирование

Запуск тестов реализуется командой:

```bash
poetry run coverage run manage.py test
```

Для проверки покрытия кода:

```bash
poetry run coverage report
```

## API Документация

- Swagger UI доступен по адресу: http://localhost:8000/swagger/
- Redoc доступен по адресу: http://localhost:8000/redoc/

## Структура проекта

```
├── config
│   ├── asgi.py
│   ├── celery.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── LICENSE
├── main
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_habit_options.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── paginators.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── services.py
│   ├── signals.py
│   ├── tasks.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_habit_model.py
│   │   ├── test_permissions.py
│   │   ├── test_send_telegram_message.py
│   │   ├── test_send_tg_notification.py
│   │   └── test_signals.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── media
├── pyproject.toml
├── README.md
├── static
└── users
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_customuser_tg_id.py
    │   ├── 0003_alter_customuser_tg_id.py
    │   ├── 0004_alter_customuser_tg_id.py
    │   ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    └── views.py
```
