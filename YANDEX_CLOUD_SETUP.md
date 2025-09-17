# 🔧 Настройка Yandex Cloud для AI Chatbot

## Шаг 1: Регистрация в Yandex Cloud

1. **Перейдите на сайт Yandex Cloud**
   - Откройте https://cloud.yandex.ru/
   - Нажмите "Войти" или "Зарегистрироваться"

2. **Создайте аккаунт**
   - Используйте ваш Яндекс аккаунт или создайте новый
   - Подтвердите email и телефон

3. **Активируйте пробный период**
   - Yandex Cloud предоставляет 3000 рублей на 60 дней
   - Этого достаточно для тестирования AI API

## Шаг 2: Создание каталога (Folder)

1. **Войдите в консоль Yandex Cloud**
   - Перейдите в https://console.cloud.yandex.ru/

2. **Создайте новый каталог**
   - Нажмите "Создать каталог"
   - Введите название: "Sakura Sushi AI"
   - Нажмите "Создать"

3. **Скопируйте ID каталога**
   - ID выглядит как `b1g1234567890abcdef`
   - Сохраните его - понадобится для настройки

## Шаг 3: Настройка AI API

### 3.1 Включение Foundation Models

1. **Перейдите в раздел AI**
   - В левом меню выберите "AI"
   - Выберите "Foundation Models"

2. **Включите YandexGPT**
   - Нажмите "Включить API"
   - Выберите ваш каталог
   - Подтвердите включение

### 3.2 Создание API ключа

1. **Перейдите в раздел "Сервисные аккаунты"**
   - В левом меню выберите "Сервисные аккаунты"
   - Нажмите "Создать сервисный аккаунт"

2. **Настройте сервисный аккаунт**
   - Имя: "sakura-sushi-ai"
   - Описание: "AI Chatbot для ресторана"
   - Нажмите "Создать"

3. **Назначьте роли**
   - Выберите созданный аккаунт
   - Перейдите на вкладку "Роли"
   - Нажмите "Назначить роли"
   - Добавьте роль: "ai.languageModels.user"
   - Нажмите "Сохранить"

4. **Создайте API ключ**
   - Выберите сервисный аккаунт
   - Перейдите на вкладку "Ключи"
   - Нажмите "Создать новый ключ"
   - Выберите "Создать API ключ"
   - Скопируйте ключ (начинается с `AQVN...`)
   - **ВАЖНО**: Сохраните ключ - он больше не будет показан!

## Шаг 4: Тестирование API

### 4.1 Проверка доступности

```bash
# Установите Yandex Cloud CLI (опционально)
curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash

# Инициализируйте CLI
yc init
```

### 4.2 Тестовый запрос к API

```python
import requests

# Ваши данные
API_KEY = "ваш-api-ключ"
FOLDER_ID = "ваш-folder-id"

# URL для API
url = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

# Заголовки
headers = {
    'Authorization': f'Api-Key {API_KEY}',
    'Content-Type': 'application/json'
}

# Данные запроса
data = {
    "modelUri": f"gpt://{FOLDER_ID}/yandexgpt",
    "completionOptions": {
        "stream": False,
        "temperature": 0.7,
        "maxTokens": 100
    },
    "messages": [
        {
            "role": "user",
            "text": "Привет! Как дела?"
        }
    ]
}

# Отправка запроса
response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## Шаг 5: Настройка переменных окружения

### 5.1 Локальная разработка

Создайте файл `.env` в корне проекта:

```env
# Yandex Cloud AI Configuration
YANDEX_CLOUD_API_KEY=AQVN1234567890abcdef...
YANDEX_CLOUD_FOLDER_ID=b1g1234567890abcdef...
YANDEX_CLOUD_MODEL_ID=yandexgpt

# Flask Configuration
FLASK_ENV=development
PORT=5000
```

### 5.2 Продакшен (Heroku)

```bash
heroku config:set YANDEX_CLOUD_API_KEY=AQVN1234567890abcdef...
heroku config:set YANDEX_CLOUD_FOLDER_ID=b1g1234567890abcdef...
heroku config:set YANDEX_CLOUD_MODEL_ID=yandexgpt
```

### 5.3 Продакшен (VPS)

```bash
# Добавьте в systemd сервис
sudo nano /etc/systemd/system/sakura-sushi.service
```

```ini
[Unit]
Description=Sakura Sushi AI Chatbot
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/api
Environment="PATH=/path/to/your/api/venv/bin"
Environment="YANDEX_CLOUD_API_KEY=AQVN1234567890abcdef..."
Environment="YANDEX_CLOUD_FOLDER_ID=b1g1234567890abcdef..."
Environment="YANDEX_CLOUD_MODEL_ID=yandexgpt"
Environment="FLASK_ENV=production"
ExecStart=/path/to/your/api/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 api:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## Шаг 6: Проверка работы

### 6.1 Запуск приложения

```bash
python api.py
```

### 6.2 Тестирование

```bash
python test_api.py
```

### 6.3 Проверка в браузере

1. Откройте http://localhost:5000
2. Нажмите на чат-бот
3. Напишите: "Привет!"
4. Проверьте ответ AI

## 🔍 Устранение неполадок

### Проблема: "API key not found"

**Решение:**
- Проверьте правильность API ключа
- Убедитесь, что ключ не содержит лишних пробелов
- Проверьте переменные окружения

### Проблема: "Folder not found"

**Решение:**
- Проверьте правильность Folder ID
- Убедитесь, что каталог существует
- Проверьте права доступа

### Проблема: "Model not available"

**Решение:**
- Убедитесь, что Foundation Models включены
- Проверьте, что у сервисного аккаунта есть роль `ai.languageModels.user`
- Попробуйте пересоздать API ключ

### Проблема: "Quota exceeded"

**Решение:**
- Проверьте лимиты в консоли Yandex Cloud
- Увеличьте квоты или перейдите на платный тариф
- Проверьте использование токенов

## 💰 Стоимость использования

### Тарифы Yandex Cloud AI (2024):

- **YandexGPT**: ~0.01$ за 1000 токенов
- **Пробный период**: 3000 рублей на 60 дней
- **Минимальная плата**: 100 рублей в месяц

### Примерные расходы:

- **1000 сообщений в день**: ~30 рублей в месяц
- **5000 сообщений в день**: ~150 рублей в месяц
- **10000 сообщений в день**: ~300 рублей в месяц

## 🔒 Безопасность

### Рекомендации:

1. **Никогда не коммитьте API ключи** в репозиторий
2. **Используйте переменные окружения** для хранения ключей
3. **Регулярно ротируйте API ключи** (каждые 3-6 месяцев)
4. **Мониторьте использование** через консоль Yandex Cloud
5. **Настройте алерты** на превышение лимитов

### Настройка мониторинга:

1. В консоли Yandex Cloud перейдите в "Мониторинг"
2. Создайте алерт на превышение квот
3. Настройте уведомления на email

## 📞 Поддержка

### Если возникли проблемы:

1. **Проверьте документацию**: https://cloud.yandex.ru/docs/
2. **Обратитесь в поддержку**: https://cloud.yandex.ru/support
3. **Сообщество**: https://t.me/yandexcloud
4. **GitHub Issues**: Создайте issue в репозитории проекта

## 🎉 Готово!

Теперь ваш AI-чатбот готов к работе с Yandex Cloud AI!

**Следующие шаги:**
- Настройте мониторинг использования
- Оптимизируйте промпты для лучших ответов
- Добавьте обработку ошибок
- Настройте резервные копии

Удачи с вашим проектом! 🤖🍣
