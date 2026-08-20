from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "place",
        "time",
        "is_pleasant",
        "periodicity",
        "is_public",
    )

    list_filter = ("is_pleasant", "is_public", "periodicity")

    search_fields = ("action", "place", "user__email")

    fields = (
        "user",
        "place",
        "time",
        "action",
        "is_pleasant",
        "related_habit",
        "periodicity",
        "reward",
        "duration",
        "is_public",
    )

