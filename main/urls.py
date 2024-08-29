from django.urls import path

from main.apps import MainConfig
from main.views import HabitListCreate, HabitRetrieveUpdateDestroy

app_name = MainConfig.name

urlpatterns = [
    path("habits/", HabitListCreate.as_view(), name="habit-list-create"),
    path(
        "habits/<int:pk>/",
        HabitRetrieveUpdateDestroy.as_view(),
        name="habit-retrieve-update-destroy",
    ),
]
