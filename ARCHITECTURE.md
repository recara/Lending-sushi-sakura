# 🏗️ Архитектура системы Sakura Sushi AI Chatbot

## Общая схема

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  🌐 Web Browser (HTML/CSS/JavaScript)                          │
│  ├── Landing Page (lend_version1.html)                         │
│  ├── Chat Interface                                            │
│  ├── Shopping Cart                                             │
│  └── Order Form                                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  🐍 Flask API Server (api.py)                                  │
│  ├── /api/chat - AI Chat Endpoint                              │
│  ├── /api/order - Order Creation                               │
│  ├── /api/menu - Menu Data                                     │
│  ├── /health - Health Check                                    │
│  └── / - Main Page                                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AI LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  🤖 Yandex Cloud AI                                            │
│  ├── YandexGPT Model                                           │
│  ├── Restaurant Context                                        │
│  ├── Conversation History                                      │
│  └── Response Generation                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Детальная архитектура

### 1. Frontend Layer (Клиентская часть)

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                │
├─────────────────────────────────────────────────────────────────┤
│  📱 Responsive HTML Landing Page                               │
│  ├── Hero Section                                              │
│  ├── Menu Section (30+ items)                                 │
│  ├── About Section                                             │
│  ├── Contact Section                                           │
│  └── Footer                                                    │
│                                                                 │
│  💬 Interactive Chat Widget                                    │
│  ├── Chat Toggle Button                                        │
│  ├── Chat Container                                            │
│  ├── Message History                                           │
│  └── Input Interface                                           │
│                                                                 │
│  🛒 Shopping Cart System                                       │
│  ├── Add to Cart Functionality                                 │
│  ├── Cart Management                                           │
│  ├── Quantity Controls                                         │
│  └── Total Calculation                                         │
│                                                                 │
│  📋 Order Form                                                 │
│  ├── Customer Information                                      │
│  ├── Delivery Details                                          │
│  ├── Payment Method                                            │
│  └── Order Submission                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Backend Layer (Серверная часть)

```
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND                                 │
├─────────────────────────────────────────────────────────────────┤
│  🐍 Flask Application (api.py)                                 │
│  ├── Request Routing                                           │
│  ├── JSON API Endpoints                                        │
│  ├── Error Handling                                            │
│  ├── Logging System                                            │
│  └── CORS Configuration                                        │
│                                                                 │
│  🔌 API Endpoints                                              │
│  ├── POST /api/chat                                            │
│  │   ├── Message Processing                                    │
│  │   ├── History Management                                    │
│  │   └── AI Integration                                        │
│  ├── POST /api/order                                           │
│  │   ├── Data Validation                                       │
│  │   ├── Order Creation                                        │
│  │   └── Response Generation                                   │
│  ├── GET /api/menu                                             │
│  │   └── Menu Data Retrieval                                   │
│  └── GET /health                                               │
│      └── System Status Check                                   │
│                                                                 │
│  🛡️ Security & Validation                                      │
│  ├── Input Sanitization                                        │
│  ├── Rate Limiting (recommended)                               │
│  ├── Error Handling                                            │
│  └── Logging & Monitoring                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 3. AI Integration Layer

```
┌─────────────────────────────────────────────────────────────────┐
│                      AI INTEGRATION                            │
├─────────────────────────────────────────────────────────────────┤
│  🤖 Yandex Cloud AI Integration                                │
│  ├── API Authentication                                        │
│  │   ├── API Key Management                                    │
│  │   └── Folder ID Configuration                               │
│  ├── Model Configuration                                       │
│  │   ├── YandexGPT Model                                       │
│  │   ├── Temperature Settings                                  │
│  │   └── Token Limits                                          │
│  ├── Context Management                                        │
│  │   ├── Restaurant Information                                │
│  │   ├── Menu Knowledge                                        │
│  │   └── Conversation History                                  │
│  └── Response Processing                                       │
│      ├── AI Response Generation                                │
│      ├── Error Handling                                        │
│      └── Fallback Responses                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Поток данных

### 1. Chat Flow (Поток чата)

```
User Input → Frontend → Flask API → Yandex AI → Response → Frontend → User
     │           │           │           │           │           │
     ▼           ▼           ▼           ▼           ▼           ▼
  "Привет"   JavaScript   /api/chat   AI Model   "Здравствуйте!"  Display
```

### 2. Order Flow (Поток заказа)

```
User Order → Frontend → Flask API → Validation → Order Creation → Response
     │           │           │           │             │             │
     ▼           ▼           ▼           ▼             ▼             ▼
  Form Data  JavaScript  /api/order  Data Check   Order ID    Success Msg
```

## Технологический стек

### Frontend
- **HTML5** - Структура страницы
- **CSS3** - Стилизация (Tailwind CSS)
- **JavaScript (ES6+)** - Интерактивность
- **Fetch API** - HTTP запросы
- **Local Storage** - Сохранение состояния

### Backend
- **Python 3.11** - Основной язык
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin requests
- **Requests** - HTTP клиент
- **Gunicorn** - WSGI сервер

### AI & Cloud
- **Yandex Cloud AI** - AI модель
- **YandexGPT** - Языковая модель
- **REST API** - Интеграция с AI

### Deployment
- **Docker** - Контейнеризация
- **Heroku** - Cloud hosting
- **Railway** - Alternative hosting
- **VPS** - Self-hosted option
- **Nginx** - Reverse proxy

## Конфигурация

### Environment Variables
```env
# Yandex Cloud AI
YANDEX_CLOUD_API_KEY=AQVN...
YANDEX_CLOUD_FOLDER_ID=b1g...
YANDEX_CLOUD_MODEL_ID=yandexgpt

# Flask
FLASK_ENV=production
PORT=5000
```

### Dependencies
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

## Масштабирование

### Горизонтальное масштабирование
```
Load Balancer (Nginx)
    ├── Flask App Instance 1
    ├── Flask App Instance 2
    └── Flask App Instance 3
```

### Вертикальное масштабирование
- Увеличение ресурсов сервера
- Оптимизация кода
- Кэширование ответов

## Мониторинг

### Health Checks
- `/health` endpoint
- AI API connectivity
- System resources

### Logging
- Request/Response logs
- Error tracking
- Performance metrics

### Metrics
- Response times
- Error rates
- AI API usage
- User interactions

## Безопасность

### API Security
- API key authentication
- Input validation
- Rate limiting
- CORS configuration

### Data Protection
- No sensitive data storage
- Secure environment variables
- HTTPS enforcement
- Error message sanitization

## Производительность

### Optimization Strategies
- Response caching
- Connection pooling
- Async processing (future)
- CDN for static assets

### Monitoring
- Response time tracking
- Memory usage monitoring
- AI API quota monitoring
- User experience metrics

## Развертывание

### Development
```bash
python api.py
```

### Production (Docker)
```bash
docker-compose up -d
```

### Production (Heroku)
```bash
git push heroku main
```

### Production (VPS)
```bash
sudo systemctl start sakura-sushi
```

## Заключение

Архитектура системы спроектирована для:
- **Производительности** - быстрые ответы AI
- **Масштабируемости** - легкое добавление инстансов
- **Надежности** - fallback механизмы
- **Безопасности** - защита данных и API
- **Простоте** - легкое развертывание и поддержка

Система готова к production использованию и может быть легко масштабирована при росте нагрузки.
