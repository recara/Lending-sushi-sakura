FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание папки для шаблонов
RUN mkdir -p templates

# Копирование HTML файла в templates
RUN cp lend_version1.html templates/

# Открытие порта
EXPOSE 5000

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "api:app"]
