from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit


class HabitTestCase(APITestCase):

    def setUp(self):
        # Создаем тестовых пользователей
        self.user = User.objects.create_user(email="test@test.ru", password="testpassword123")
        self.other_user = User.objects.create_user(email="other@test.ru", password="testpassword123")

        # Авторизуем основного пользователя в клиенте тестов
        self.client.force_authenticate(user=self.user)

        # Создаем тестовую приятную привычку для проверок связанных привычек
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            time="08:00:00",
            action="Принять ванну",
            is_pleasant=True,
            periodicity=1
        )

    def test_create_habit(self):
        """Тестирование создания полезной привычки со связанной приятной привычкой"""

        url = reverse("habits:habit-create")
        data = {
            "place": "Спортзал",
            "time": "18:00:00",
            "action": "Сделать приседания",
            "related_habit": self.pleasant_habit.id,
            "periodicity": 1,
            "duration": "00:01:00"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(action="Сделать приседания").count(), 1)

    def test_habit_validators(self):
        """Тестирование валидатора: одновременно награда и связанная привычка"""

        url = reverse("habits:habit-create")
        data = {
            "place": "Спортзал",
            "time": "18:00:00",
            "action": "Ошибка валидации",
            "related_habit": self.pleasant_habit.id,
            "reward": "Съесть шоколадку",  # Ошибка: нельзя указывать и то, и то
            "periodicity": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_list_and_pagination(self):
        """Тестирование получения списка привычек и структуры пагинации DRF"""

        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем структуру пагинации, которая требуется по критериям ТЗ
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

    def test_other_user_permissions(self):
        """Тестирование прав доступа: пользователь не может удалить чужую привычку"""

        # Создаем приватную привычку основного пользователя
        private_habit = Habit.objects.create(
            user=self.user, place="Дома", time="12:00:00", action="Секретное действие", periodicity=1
        )
        # Переключаем клиента на другого пользователя
        self.client.force_authenticate(user=self.other_user)
        url = reverse("habits:habit-delete", kwargs={"pk": private_habit.pk})

        response = self.client.delete(url)
        # Система должна вернуть 403 Forbidden согласно кастомному IsOwner пермишену
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

