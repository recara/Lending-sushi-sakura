# 🚀 Быстрый старт - Sakura Sushi AI Chatbot

## Шаг 1: Подготовка Yandex Cloud

1. **Регистрация в Yandex Cloud**
   - Перейдите на https://cloud.yandex.ru/
   - Создайте аккаунт или войдите

2. **Создание каталога**
   - В консоли создайте новый каталог
   - Скопируйте ID каталога (выглядит как `b1g...`)

3. **Настройка AI API**
   - Перейдите в "AI" → "Foundation Models"
   - Включите YandexGPT
   - Создайте API ключ

## Шаг 2: Локальный запуск

```bash
# 1. Клонируйте проект
git clone <your-repo-url>
cd api

# 2. Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Создайте .env файл
cp config.env.example .env

# 5. Отредактируйте .env файл
nano .env  # или любой текстовый редактор
```

**Содержимое .env файла:**
```env
YANDEX_CLOUD_API_KEY=ваш-реальный-api-ключ
YANDEX_CLOUD_FOLDER_ID=ваш-реальный-folder-id
YANDEX_CLOUD_MODEL_ID=yandexgpt
FLASK_ENV=development
PORT=5000
```

```bash
# 6. Запустите сервер
python api.py

# 7. Откройте браузер
# http://localhost:5000
```

## Шаг 3: Тестирование

1. **Откройте сайт** в браузере
2. **Нажмите на чат-бот** (иконка в правом нижнем углу)
3. **Напишите сообщение**: "Привет, что у вас есть?"
4. **Проверьте ответ** AI-консультанта

## Шаг 4: Деплой на Heroku (самый простой способ)

```bash
# 1. Установите Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Войдите в Heroku
heroku login

# 3. Создайте приложение
heroku create your-app-name

# 4. Добавьте переменные окружения
heroku config:set YANDEX_CLOUD_API_KEY=ваш-api-ключ
heroku config:set YANDEX_CLOUD_FOLDER_ID=ваш-folder-id
heroku config:set FLASK_ENV=production

# 5. Деплой
git add .
git commit -m "Initial deployment"
git push heroku main

# 6. Откройте приложение
heroku open
```

## Шаг 5: Деплой на VPS (для продвинутых)

```bash
# 1. Подключитесь к серверу
ssh user@your-server-ip

# 2. Установите зависимости
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx git -y

# 3. Клонируйте проект
git clone <your-repo-url>
cd api

# 4. Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 5. Установите зависимости
pip install -r requirements.txt

# 6. Создайте .env файл
nano .env
# Добавьте ваши переменные окружения

# 7. Создайте systemd сервис
sudo nano /etc/systemd/system/sakura-sushi.service
```

**Содержимое сервиса:**
```ini
[Unit]
Description=Sakura Sushi AI Chatbot
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/user/api
Environment="PATH=/home/user/api/venv/bin"
ExecStart=/home/user/api/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 api:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 8. Запустите сервис
sudo systemctl enable sakura-sushi
sudo systemctl start sakura-sushi

# 9. Настройте Nginx
sudo nano /etc/nginx/sites-available/sakura-sushi
```

**Конфигурация Nginx:**
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
# 10. Активируйте конфигурацию
sudo ln -s /etc/nginx/sites-available/sakura-sushi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🎯 Проверка работы

После деплоя проверьте:

1. **Главная страница** загружается
2. **Чат-бот** отвечает на сообщения
3. **Корзина** работает
4. **Оформление заказа** функционирует
5. **Health check**: `https://your-domain.com/health`

## 🔧 Устранение неполадок

### Проблема: AI не отвечает
- Проверьте API ключ Yandex Cloud
- Убедитесь, что Folder ID правильный
- Проверьте логи: `heroku logs --tail` или `sudo journalctl -u sakura-sushi -f`

### Проблема: Сайт не загружается
- Проверьте переменные окружения
- Убедитесь, что порт 5000 открыт
- Проверьте статус сервиса: `sudo systemctl status sakura-sushi`

### Проблема: Ошибки в логах
- Проверьте синтаксис Python кода
- Убедитесь, что все зависимости установлены
- Проверьте права доступа к файлам

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи приложения
2. Убедитесь в правильности переменных окружения
3. Создайте issue в репозитории
4. Обратитесь к документации Yandex Cloud

## 🎉 Готово!

Ваш AI-чатбот для ресторана готов к работе! 

**Следующие шаги:**
- Настройте домен и SSL сертификат
- Добавьте аналитику (Google Analytics)
- Настройте мониторинг (Uptime Robot)
- Создайте резервные копии

Удачи с вашим проектом! 🍣🤖
