from rest_framework import serializers
from habits.models import Habit
from habits.validators import (
    RewardAndRelatedHabitValidator,
    DurationValidator,
    OnlyPleasantRelatedHabitValidator,
    PleasantHabitRestrictionsValidator,
    PeriodicityValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardAndRelatedHabitValidator(),
            DurationValidator(),
            OnlyPleasantRelatedHabitValidator(),
            PleasantHabitRestrictionsValidator(),
            PeriodicityValidator(),
        ]
