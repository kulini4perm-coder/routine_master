from datetime import timedelta
from django.conf import settings
from django.db import models


class Habit(models.Model):
    # Пользователь
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Создатель привычки",
    )

    # Место, где необходимо выполнять привычку
    place = models.CharField(
        max_length=255,
        verbose_name="Место выполнения",
        help_text="Например: дома, в спортзале, в офисе",
    )

    # Время, когда необходимо выполнять привычку
    time = models.TimeField(
        verbose_name="Время выполнения", help_text="Укажите время суток"
    )

    # Действие, которое представляет собой привычка
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Например: сделать 20 приседаний, выпить стакан воды",
    )

    # Признак приятной привычки
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Отметьте, если привычка является приятной (вознаграждением)",
    )

    # Связанная привычка
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="useful_habits",
        verbose_name="Связанная привычка",
        help_text="Привяжите приятную привычку к полезной",
    )

    # Периодичность (в днях, по умолчанию ежедневная = 1)
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
        help_text="Интервал выполнения привычки в днях (по умолчанию 1 — каждый день)",
    )

    # Вознаграждение
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Чем вы себя вознаградите, если нет связанной приятной привычки",
    )

    # Время на выполнение
    duration = models.DurationField(
        default=timedelta(minutes=2),
        verbose_name="Время на выполнение",
        help_text="Сколько времени займет выполнение (не более 2 минут)",
    )

    # Признак публичности
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Сделать привычку видимой для всех пользователей",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("id",)

    def __str__(self):
        return f"{self.user} будет {self.action} в {self.time} в {self.place}"

