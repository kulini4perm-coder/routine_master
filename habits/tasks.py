from datetime import datetime
from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminders():
    """ Периодическая задача: каждую минуту проверяет текущее время,
    находит привычки и отправляет напоминания """

    # Получаем текущее время
    current_time = timezone.localtime(timezone.now()).time()
    current_hour_minute = current_time.replace(second=0, microsecond=0)

    # Ищем привычки, у которых время совпадает с текущим (минута в минуту),
    # а у создателя привычки заполнен уникальный tg_chat_id
    habits_to_remind = Habit.objects.filter(
        time__hour=current_hour_minute.hour,
        time__minute=current_hour_minute.minute,
        user__tg_chat_id__isnull=False,
    )

    for habit in habits_to_remind:
        # Формируем текст сообщения
        message_text = (
            f"\nПривет! Время выработать полезный ритуал!\n"
            f"Напоминание: я буду [{habit.action}] в [{habit.time.strftime('%H:%M')}] в [{habit.place}]."
        )

        # Если есть вознаграждение, добавляем мотивацию
        if habit.reward:
            message_text += f"\nНаграда после выполнения: {habit.reward}"
        elif habit.related_habit:
            message_text += (
                f"\n🎉 Сразу после этого сделай приятное: {habit.related_habit.action}"
            )

        # Вызываем наш сервис отправки
        send_telegram_message(
            chat_id=habit.user.tg_chat_id, text=message_text
        )

    return f"Проверка завершена. Отправлено напоминаний: {habits_to_remind.count()}."
