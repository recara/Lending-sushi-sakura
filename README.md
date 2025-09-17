# Sakura Sushi - AI Chatbot для ресторана

Интеллектуальный чат-бот для ресторана японской кухни с интеграцией Yandex Cloud AI.

## 🚀 Возможности

- **AI-консультант** на базе YandexGPT
- **Интерактивное меню** с корзиной покупок
- **Онлайн заказы** с доставкой
- **Адаптивный дизайн** для всех устройств
- **Многоязычная поддержка** (русский)

## 🛠 Технологии

- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Backend**: Python Flask
- **AI**: Yandex Cloud AI (YandexGPT)
- **Deployment**: Docker, Heroku, Railway, VPS

## 📋 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd api
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
```bash
cp config.env.example .env
# Отредактируйте .env файл с вашими данными Yandex Cloud
```

### 4. Запуск локально
```bash
python api.py
```

Откройте http://localhost:5000 в браузере.

## 🔧 Настройка Yandex Cloud

1. Создайте аккаунт в [Yandex Cloud](https://cloud.yandex.ru/)
2. Создайте каталог и получите Folder ID
3. Включите AI API и создайте API ключ
4. Добавьте данные в файл `.env`

## 🚀 Деплой

### Heroku
```bash
heroku create your-app-name
heroku config:set YANDEX_CLOUD_API_KEY=your-key
heroku config:set YANDEX_CLOUD_FOLDER_ID=your-folder-id
git push heroku main
```

### Docker
```bash
docker-compose up -d
```

### VPS
Следуйте инструкциям в [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📁 Структура проекта

```
api/
├── api.py                 # Flask приложение
├── lend_version1.html     # HTML лендинг
├── requirements.txt       # Python зависимости
├── Dockerfile            # Docker конфигурация
├── docker-compose.yml    # Docker Compose
├── Procfile             # Heroku конфигурация
├── config.env.example   # Пример переменных окружения
└── DEPLOYMENT_GUIDE.md  # Подробное руководство по деплою
```

## 🔌 API Endpoints

- `GET /` - Главная страница
- `POST /api/chat` - Чат с AI
- `POST /api/order` - Создание заказа
- `GET /api/menu` - Получение меню
- `GET /health` - Проверка состояния

## 💡 Примеры использования

### Чат с AI
```javascript
fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Рекомендуйте роллы',
    history: []
  })
})
```

### Создание заказа
```javascript
fetch('/api/order', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Иван Иванов',
    phone: '+79123456789',
    address: 'г. Владивосток, ул. Светланская, 42',
    items: [{ name: 'Филадельфия', price: 490, quantity: 1 }],
    total: 490
  })
})
```

## 🔒 Безопасность

- API ключи хранятся в переменных окружения
- HTTPS обязательно для продакшена
- Rate limiting для защиты от спама
- Валидация входных данных

## 📊 Мониторинг

- Health check endpoint: `/health`
- Логирование всех запросов
- Отслеживание ошибок
- Метрики производительности

## 🤝 Поддержка

- Создайте issue для багов
- Pull requests приветствуются
- Документация в DEPLOYMENT_GUIDE.md

## 📄 Лицензия

MIT License

## 🎯 Roadmap

- [ ] Интеграция с базой данных
- [ ] Система уведомлений
- [ ] Аналитика заказов
- [ ] Многоязычность
- [ ] Мобильное приложение

---

**Создано с ❤️ для ресторана Sakura Sushi**
