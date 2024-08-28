from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    """
    Пагинатор для объектов Habit.

    Разбивает вывод списка привычек на страницы с 5 привычками на каждой странице.
    """

    page_size = 5
