FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Настройки Python и переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем и обновляем pip, ставим Poetry
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir "poetry>=1.8.3"

# Копируем файлы зависимостей в контейнер
COPY pyproject.toml poetry.lock* requirements.txt* ./

# Если есть requirements.txt — ставим через pip, если нет — через Poetry
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        poetry install --no-root --no-interaction --no-ansi; \
    fi

# Копируем исходный код приложения в контейнер
COPY . .

# Создаем директории для статики и медиафайлов
RUN mkdir -p /app/staticfiles /app/media

# Пробрасываем порт
EXPOSE 8000

# Команда для запуска приложения через сервер Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
