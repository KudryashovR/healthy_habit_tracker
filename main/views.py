from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from main.models import Habit
from main.paginators import HabitPagination
from main.permissions import IsOwnerOrReadOnly
from main.serializers import HabitSerializer


class HabitListCreate(generics.ListCreateAPIView):
    """
    Представление для отображения списка привычек и создания новой привычки.

    Доступ предоставляет:
    - Для GET-запросов: отображает список привычек текущего пользователя и публичные привычки.
    - Для POST-запросов: позволяет текущему пользователю создать новую привычку.

    Атрибуты:
    - serializer_class: сериализатор, используемый для представления и валидации данных о привычках.
    - pagination_class: класс пагинации для разделения списка привычек на страницы.
    - permission_classes: указание, что пользователь должен быть аутентифицирован (авторизован).

    Методы:
    - get_queryset: возвращает привычки, принадлежащие пользователю, или публичные привычки.
    - perform_create: автоматически устанавливает текущего пользователя владельцем создаваемой привычки.
    """

    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user) | Habit.objects.filter(
            is_public=True
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HabitRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления конкретной привычки.

    Доступ предоставляет:
    - Для GET-запросов: отображает информацию о выбранной привычке.
    - Для PUT/PATCH-запросов: позволяет обновить данные привычки только её владельцу.
    - Для DELETE-запросов: позволяет удалить привычку только её владельцу.

    Атрибуты:
    - queryset: полный набор привычек для выборки объекта.
    - serializer_class: сериализатор, используемый для представления и валидации данных о привычках.
    - permission_classes: указание, что пользователь должен быть аутентифицирован (авторизован) и что изменения может
                          делать только владелец привычки.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
