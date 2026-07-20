from django.urls import path

from habits.views import (
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    PublicHabitListAPIView,
)

app_name = "habits"

urlpatterns = [
    path("", HabitListAPIView.as_view(), name="habit-list"),
    path("create/", HabitCreateAPIView.as_view(), name="habit-create"),
    path("public/", PublicHabitListAPIView.as_view(), name="habit-public"),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit-get"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habit-update"),
    path("<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habit-delete"),
]
