from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime
import logging

# === Настройка логирования ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Инициализация приложения ===
# Указываем, что шаблоны находятся в корневой папке
app = Flask(__name__, template_folder='.')

# Включаем CORS для всех маршрутов
CORS(app)

# === Конфигурация Yandex Cloud ===
YANDEX_CLOUD_API_KEY = os.getenv('YANDEX_CLOUD_API_KEY', 'your-api-key-here')
YANDEX_CLOUD_FOLDER_ID = os.getenv('YANDEX_CLOUD_FOLDER_ID', 'your-folder-id-here')
YANDEX_CLOUD_MODEL_ID = os.getenv('YANDEX_CLOUD_MODEL_ID', 'yandexgpt')

# 🔧 ВАЖНО: убраны пробелы в конце URL!
YANDEX_AI_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

# === Контекст для AI модели ===
RESTAURANT_CONTEXT = """
Ты - AI-консультант ресторана японской кухни "Sakura Sushi" во Владивостоке.

О ресторане:
- Специализация: суши, роллы, японская кухня
- Адрес: г. Владивосток, ул. Светланская, 42
- Телефон: +7 (423) 200-12-34
- Часы работы: Пн-Вс: 10:00 - 23:00
- Доставка: 45 минут в будни, 60 минут в выходные
- Минимальная сумма заказа: 900 ₽
- Бесплатная доставка от 1500 ₽

Популярные блюда:
- Филадельфия (490 ₽) - лосось, сливочный сыр, авокадо, огурец
- Сет Самурай (1390 ₽) - 30 шт.: Филадельфия, Калифорния, Темпура, Чиз ролл
- Рамен (450 ₽) - куриный бульон, лапша, яйцо, нори, свинина Чашу
- Мисо суп (190 ₽) - тофу, вакаме, зеленый лук, бульон мисо
- Сашими (560 ₽) - свежий лосось, тунец и окунь
- Темпура ролл (520 ₽) - ролл с креветкой в хрустящей панировке
- Ролл Дракон (620 ₽) - угорь, авокадо, огурец, соус унаги

Твоя задача:
1. Помогать клиентам с выбором блюд
2. Отвечать на вопросы о составе, цене, доставке
3. Принимать заказы (собирать телефон и адрес)
4. Рассказывать об акциях и новинках
5. Быть дружелюбным и профессиональным

Отвечай кратко и по делу. Если клиент хочет заказать, попроси телефон и адрес.
"""

def call_yandex_ai(user_message, conversation_history=None):
    """Вызов AI модели Yandex Cloud"""
    try:
        headers = {
            'Authorization': f'Api-Key {YANDEX_CLOUD_API_KEY}',
            'Content-Type': 'application/json'
        }

        system_prompt = RESTAURANT_CONTEXT

        if conversation_history:
            history_text = "\n".join([
                f"Клиент: {msg['user']}\nКонсультант: {msg['bot']}"
                for msg in conversation_history[-5:]
            ])
            system_prompt += f"\n\nИстория разговора:\n{history_text}"

        system_prompt += f"\n\nКлиент: {user_message}\nКонсультант:"

        data = {
            "modelUri": f"gpt://{YANDEX_CLOUD_FOLDER_ID}/{YANDEX_CLOUD_MODEL_ID}",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 500
            },
            "messages": [
                {
                    "role": "system",
                    "text": system_prompt
                }
            ]
        }

        response = requests.post(YANDEX_AI_URL, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            return result['result']['alternatives'][0]['message']['text'].strip()
        else:
            logger.error(f"Yandex AI API error: {response.status_code} - {response.text}")
            return "Извините, произошла техническая ошибка. Попробуйте позже."

    except Exception as e:
        logger.error(f"Error calling Yandex AI: {str(e)}")
        return "Извините, произошла техническая ошибка. Попробуйте позже."


@app.route('/')
def index():
    """Главная страница — отдаем HTML из корня"""
    try:
        return render_template('lend_version1.html')
    except Exception as e:
        logger.error(f"Template not found: {e}")
        return f"<h1 style='color:red'>Ошибка: не найден lend_version1.html</h1><p>{str(e)}</p>", 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint для чата с AI"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])

        if not user_message:
            return jsonify({'error': 'Сообщение не может быть пустым'}), 400

        ai_response = call_yandex_ai(user_message, conversation_history)
        logger.info(f"User: {user_message} → AI: {ai_response}")

        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Chat API error: {str(e)}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


@app.route('/api/order', methods=['POST'])
def create_order():
    """API endpoint для создания заказа"""
    try:
        data = request.get_json()

        required_fields = ['name', 'phone', 'address', 'items']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Поле "{field}" обязательно'}), 400

        order_id = f"ORDER_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        order_data = {
            'id': order_id,
            'customer': {
                'name': data['name'],
                'phone': data['phone'],
                'email': data.get('email', ''),
                'address': data['address']
            },
            'items': data['items'],
            'total': data.get('total', 0),
            'delivery_time': data.get('delivery_time', 'asap'),
            'payment_method': data.get('payment_method', 'cash'),
            'comment': data.get('comment', ''),
            'status': 'new',
            'created_at': datetime.now().isoformat()
        }

        logger.info(f"✅ Новый заказ создан: {order_id}")
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'Заказ успешно оформлен!'
        })

    except Exception as e:
        logger.error(f"Order API error: {str(e)}")
        return jsonify({'error': 'Ошибка при создании заказа'}), 500


@app.route('/api/menu', methods=['GET'])
def get_menu():
    """API endpoint для получения меню"""
    menu_items = [
        {
            'id': 1,
            'name': 'Филадельфия',
            'description': 'Лосось, сливочный сыр, авокадо, огурец. 8 шт., 250 г.',
            'price': 490,
            'category': 'rolls',
            'image': 'https://avatars.mds.yandex.net/i?id=8576130dcdd13973095d8c75482182f6e93a19df-4854935-images-thumbs&n=13'
        },
        {
            'id': 2,
            'name': 'Сет Самурай',
            'description': '30 шт.: Филадельфия, Калифорния, Темпура, Чиз ролл. 950 г.',
            'price': 1390,
            'category': 'rolls',
            'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/max_3840/7431b582203759.5d1607ad5a3c2.jpg'
        },
        {
            'id': 3,
            'name': 'Рамен',
            'description': 'Куриный бульон, лапша, яйцо, нори, свинина Чашу. 400 г.',
            'price': 450,
            'category': 'noodles',
            'image': 'https://avatars.mds.yandex.net/i?id=b6eec287b79f84376c9500a1f5c064f76b435b24-10779221-images-thumbs&n=13'
        },
        {
            'id': 4,
            'name': 'Мисо суп',
            'description': 'Тофу, вакаме, зеленый лук, бульон мисо. 250 мл.',
            'price': 190,
            'category': 'soups',
            'image': 'https://avatars.mds.yandex.net/i?id=4e7cfdd02e83ebb1b54d9a6c7dfb98c3299dc9e9-16447530-images-thumbs&n=13'
        },
        {
            'id': 5,
            'name': 'Сашими',
            'description': 'Свежий лосось, тунец и окунь. 150 г.',
            'price': 560,
            'category': 'sashimi',
            'image': 'https://avatars.mds.yandex.net/i?id=cd6f8c1e01fbca2cc24618523660d7de2baa4230-4393404-images-thumbs&n=13'
        }
    ]
    return jsonify({'menu': menu_items})


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'yandex_ai_configured': bool(YANDEX_CLOUD_API_KEY and YANDEX_CLOUD_FOLDER_ID),
        'version': '1.0'
    })


# === Запуск приложения (для Render / VK Cloud) ===
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    logger.info(f"🚀 Сервер запущен на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
