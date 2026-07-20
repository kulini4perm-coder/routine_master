from datetime import timedelta
from rest_framework.serializers import ValidationError


class RewardAndRelatedHabitValidator:
    """ Исключает одновременный выбор вознаграждения и связанной привычки """

    def __call__(self, value):
        reward = value.get("reward")
        related_habit = value.get("related_habit")
        is_pleasant = value.get("is_pleasant", False)

        # Проверка для полезных привычек
        if not is_pleasant:
            if reward and related_habit:
                raise ValidationError(
                    "Нельзя одновременно указать вознаграждение и связанную привычку. Выберите что-то одно."
                )
            if not reward and not related_habit:
                raise ValidationError(
                    "У полезной привычки должно быть заполнено либо поле вознаграждения, либо связанная привычка."
                )


class DurationValidator:
    """ Ограничивает время выполнения привычки """

    def __call__(self, value):
        duration = value.get("duration")

        if duration and duration > timedelta(seconds=120):
            raise ValidationError(
                "Время выполнения привычки не должно превышать 120 секунд (2 минуты)."
            )


class OnlyPleasantRelatedHabitValidator:
    """ В связанные привычки могут попадать только приятные привычки """

    def __call__(self, value):
        related_habit = value.get("related_habit")

        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                "В поле 'Связанная привычка' можно добавить только приятную привычку"
            )


class PleasantHabitRestrictionsValidator:
    """ У приятной привычки не может быть своего вознаграждения или своей связанной привычки """

    def __call__(self, value):
        is_pleasant = value.get("is_pleasant", False)
        reward = value.get("reward")
        related_habit = value.get("related_habit")

        if is_pleasant:
            if reward or related_habit:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )


class PeriodicityValidator:
    """ Нельзя выполнять привычку реже, чем 1 раз в 7 дней """

    def __call__(self, value):
        periodicity = value.get("periodicity")

        if periodicity and periodicity > 7:
            raise ValidationError(
                "Привычку нужно выполнять хотя бы раз в неделю."
            )
