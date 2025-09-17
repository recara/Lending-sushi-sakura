# Руководство по развертыванию AI-чатбота для ресторана Sakura Sushi

## Обзор проекта

Этот проект представляет собой веб-приложение для ресторана японской кухни с интегрированным AI-чатботом, использующим Yandex Cloud AI API. Приложение состоит из:

- **Frontend**: HTML лендинг с интерактивным чатом
- **Backend**: Flask API сервер с интеграцией Yandex Cloud AI
- **AI**: YandexGPT для обработки сообщений клиентов

## Архитектура системы

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTML Client   │◄──►│   Flask API     │◄──►│ Yandex Cloud AI │
│   (Frontend)    │    │   (Backend)     │    │   (AI Model)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Предварительные требования

### 1. Yandex Cloud настройка

1. **Создайте аккаунт в Yandex Cloud**
   - Перейдите на https://cloud.yandex.ru/
   - Зарегистрируйтесь или войдите в аккаунт

2. **Создайте каталог (Folder)**
   - В консоли Yandex Cloud создайте новый каталог
   - Запомните ID каталога

3. **Настройте AI API**
   - Перейдите в раздел "AI" → "Foundation Models"
   - Включите API для YandexGPT
   - Создайте API ключ

4. **Получите необходимые данные**
   - API ключ (YANDEX_CLOUD_API_KEY)
   - ID каталога (YANDEX_CLOUD_FOLDER_ID)

### 2. Локальная разработка

```bash
# Клонируйте проект
git clone <your-repo-url>
cd api

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установите зависимости
pip install -r requirements.txt

# Создайте файл .env
cp config.env.example .env
# Отредактируйте .env файл с вашими данными
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Yandex Cloud AI Configuration
YANDEX_CLOUD_API_KEY=your-actual-api-key-here
YANDEX_CLOUD_FOLDER_ID=your-actual-folder-id-here
YANDEX_CLOUD_MODEL_ID=yandexgpt

# Flask Configuration
FLASK_ENV=development
PORT=5000
```

## Локальный запуск

```bash
# Запустите сервер
python api.py

# Откройте браузер
http://localhost:5000
```

## Варианты хостинга

### 1. Heroku (Рекомендуется для начинающих)

#### Подготовка к деплою:

1. **Создайте Procfile**:
```bash
echo "web: gunicorn api:app" > Procfile
```

2. **Создайте runtime.txt**:
```bash
echo "python-3.11.0" > runtime.txt
```

3. **Деплой на Heroku**:
```bash
# Установите Heroku CLI
# Создайте приложение
heroku create your-app-name

# Добавьте переменные окружения
heroku config:set YANDEX_CLOUD_API_KEY=your-api-key
heroku config:set YANDEX_CLOUD_FOLDER_ID=your-folder-id
heroku config:set FLASK_ENV=production

# Деплой
git add .
git commit -m "Initial deployment"
git push heroku main
```

### 2. Railway

1. **Подключите GitHub репозиторий**
2. **Настройте переменные окружения** в панели Railway
3. **Деплой автоматический** при push в main ветку

### 3. DigitalOcean App Platform

1. **Создайте приложение** в DigitalOcean
2. **Подключите GitHub репозиторий**
3. **Настройте переменные окружения**
4. **Деплой автоматический**

### 4. VPS (VDS) хостинг

#### Настройка Ubuntu/Debian сервера:

```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите Python и pip
sudo apt install python3 python3-pip python3-venv nginx -y

# Клонируйте проект
git clone <your-repo-url>
cd api

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте systemd сервис
sudo nano /etc/systemd/system/sakura-sushi.service
```

**Содержимое файла сервиса**:
```ini
[Unit]
Description=Sakura Sushi AI Chatbot
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/api
Environment="PATH=/path/to/your/api/venv/bin"
ExecStart=/path/to/your/api/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 api:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Настройка Nginx**:
```bash
sudo nano /etc/nginx/sites-available/sakura-sushi
```

**Конфигурация Nginx**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Активируйте конфигурацию
sudo ln -s /etc/nginx/sites-available/sakura-sushi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Запустите сервис
sudo systemctl enable sakura-sushi
sudo systemctl start sakura-sushi
```

### 5. Docker деплой

**Создайте Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api:app"]
```

**Создайте docker-compose.yml**:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - YANDEX_CLOUD_API_KEY=${YANDEX_CLOUD_API_KEY}
      - YANDEX_CLOUD_FOLDER_ID=${YANDEX_CLOUD_FOLDER_ID}
      - FLASK_ENV=production
    restart: unless-stopped
```

**Запуск**:
```bash
docker-compose up -d
```

## Мониторинг и логирование

### 1. Логирование

Приложение автоматически логирует:
- Запросы к AI API
- Ошибки
- Созданные заказы

### 2. Health Check

Доступен endpoint `/health` для проверки состояния:
```bash
curl https://your-domain.com/health
```

### 3. Мониторинг производительности

Рекомендуется использовать:
- **Uptime Robot** - мониторинг доступности
- **Sentry** - отслеживание ошибок
- **Google Analytics** - аналитика пользователей

## Безопасность

### 1. Переменные окружения
- Никогда не коммитьте API ключи в репозиторий
- Используйте `.env` файлы для локальной разработки
- Настройте переменные окружения на продакшене

### 2. HTTPS
- Обязательно используйте SSL сертификаты
- Настройте автоматическое перенаправление с HTTP на HTTPS

### 3. Rate Limiting
Рекомендуется добавить ограничение запросов:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # ... ваш код
```

## Масштабирование

### 1. Горизонтальное масштабирование
- Используйте несколько экземпляров приложения
- Настройте load balancer (Nginx, HAProxy)
- Используйте Redis для сессий

### 2. База данных
Для продакшена рекомендуется добавить:
- PostgreSQL для хранения заказов
- Redis для кэширования

### 3. CDN
- Используйте CloudFlare или AWS CloudFront
- Оптимизируйте статические ресурсы

## Стоимость хостинга

### Примерные цены (2024):

1. **Heroku**: $7-25/месяц
2. **Railway**: $5-20/месяц  
3. **DigitalOcean**: $5-12/месяц
4. **VPS**: $3-10/месяц
5. **Yandex Cloud AI**: ~$0.01 за 1000 токенов

## Поддержка и обновления

### 1. Обновление кода
```bash
git pull origin main
pip install -r requirements.txt
# Перезапустите сервис
```

### 2. Мониторинг логов
```bash
# Heroku
heroku logs --tail

# VPS
sudo journalctl -u sakura-sushi -f
```

### 3. Резервное копирование
- Настройте автоматические бэкапы базы данных
- Сохраняйте конфигурационные файлы
- Документируйте изменения

## Заключение

Этот проект предоставляет полнофункциональное решение для ресторана с AI-чатботом. Выберите подходящий вариант хостинга в зависимости от ваших потребностей и бюджета.

Для получения поддержки создайте issue в репозитории или обратитесь к документации используемых сервисов.
