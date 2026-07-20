import os
import requests


def send_telegram_message(chat_id: str, text: str) -> None:
    """ Отправляет текстовое сообщение пользователю в Telegram.
    Режим без токена и рабочий режим """

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    api_url = os.getenv("TELEGRAM_API_URL", "https://telegram.org")

    # Режим без токена для тестирования
    if not bot_token:
        print("\n" + "=" * 50)
        print("[MOCK TELEGRAM BOT] Имитация отправки напоминания:")
        print(f"Кому (Chat ID): {chat_id}")
        print(f"Текст сообщения: {text}")
        print("=" * 50 + "\n")
        return

    # Рабочий режим: отправка реального запроса к API Telegram
    url = f"{api_url}{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Не удалось отправить сообщение в Telegram: {e}")
