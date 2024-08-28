from django.core.exceptions import ValidationError
from django.db import models

from users.models import CustomUser


class Habit(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='habits', verbose_name='владелец')
    place = models.CharField(max_length=255, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=255, verbose_name='действие')
    is_pleasant_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='related_habits', verbose_name='связанная привычка')
    frequency = models.PositiveIntegerField(default=1, verbose_name='периодичность', help_text='в днях')
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name='вознаграждение')
    time_to_complete = models.PositiveIntegerField(verbose_name='время на выполнение',
                                            help_text='секунд')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return self.action

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError(
                "Вы не можете установить одновременно связанную привычку и вознаграждение. Должно быть заполнено только одно из полей.")

        if self.is_pleasant_habit and (self.related_habit or self.reward):
            raise ValidationError("Приятная привычка не может иметь связанной с ней привычки или награды.")

        if self.frequency > 7:
            raise ValidationError("Привычку нельзя выполнять реже, чем раз в 7 дней.")

        if self.time_to_complete > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")

        super().clean()

    class Meta:
        verbose_name = 'пивычка'
        verbose_name_plural = 'пивычки'
