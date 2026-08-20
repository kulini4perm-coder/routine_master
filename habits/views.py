from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer

from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Создание новой привычки",
    description="Принимает параметры привычки и привязывает текущего авторизованного пользователя как владельца."
)
class HabitCreateAPIView(generics.CreateAPIView):
    """ Создание новой привычки авторизованным пользователем """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Привязка текущего пользователя к создаваемой привычке
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Список личных привычек пользователя",
    description="Возвращает постраничный список (по 5 элементов) привычек текущего авторизованного пользователя."
)
class HabitListAPIView(generics.ListAPIView):
    """ Получение списка личных привычек текущего пользователя, пагинация по 5 привычек на страницу """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get_queryset(self):
        # Возвращаем привычки текущего пользователя
        return Habit.objects.filter(user=self.request.user)


@extend_schema(
    summary="Список всех публичных привычек",
    description="Возвращает постраничный список (по 5 элементов) привычек всех пользователей системы"
)
class PublicHabitListAPIView(generics.ListAPIView):
    """ Просмотр списка всех публичных привычек """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get_queryset(self):
        # Возвращаем привычки, у которых признак публичности равен True
        return Habit.objects.filter(is_public=True)


@extend_schema(
    summary="Детальная информация о привычке",
    description="Возвращает полную структуру полей конкретной привычки по её ID. Доступно только владельцу."
)
class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр владельцем деталей конкретной привычки по ID """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


@extend_schema(
    summary="Редактирование привычки",
    description="Позволяет полностью или частично обновить поля привычки."
)
class HabitUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование привычки владельцем """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


@extend_schema(
    summary="Удаление привычки",
    description="Безвозвратно удаляет привычку из базы данных по её ID. Доступно только владельцу."
)
class HabitDestroyAPIView(generics.DestroyAPIView):
    """ Удаление привычки владельцем """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

