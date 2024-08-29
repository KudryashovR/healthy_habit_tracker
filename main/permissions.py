from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Класс разрешений, позволяющий только владельцу объекта редактировать его.

    Разрешает доступ на чтение (GET, HEAD, OPTIONS) любым пользователям, но разрешает доступ на изменение (POST, PUT,
    PATCH, DELETE) только в том случае, если текущий пользователь является владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет разрешения для конкретного объекта.

        Аргументы:
            request: Текущий запрос.
            view: Представление, в котором используется разрешение.
            obj: Текущий объект, к которому осуществляется доступ.

        Возвращает:
            bool: True, если запрос является безопасным методом (т.е. только на чтение), или если текущий пользователь
                  является владельцем объекта. Иначе False.
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
