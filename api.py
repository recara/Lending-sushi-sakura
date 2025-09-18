from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime
import logging

# === Настройка логирования ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Инициализация приложения ===
app = Flask(__name__, template_folder='.')
CORS(app)

# === Конфигурация Yandex Cloud ===
YANDEX_CLOUD_FOLDER_ID = os.getenv('YANDEX_CLOUD_FOLDER_ID', 'b1ga94okgf6e5d8edu0u')
IAM_TOKEN = os.getenv('IAM_TOKEN')  # Можно использовать IAM-токен
API_KEY = os.getenv('YANDEX_API_KEY')  # Или API-ключ

# URL для Yandex GPT
YANDEX_AI_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

# Модель: yandexgpt-lite/latest
MODEL_URI = f"gpt://{YANDEX_CLOUD_FOLDER_ID}/yandexgpt-lite/latest"

# Контекст AI
RESTAURANT_CONTEXT = """
Ты - AI-консультант ресторана японской кухни "Sakura Sushi" во Владивостоке.
Отвечай кратко, дружелюбно, помоги клиентам с выбором блюд, ценой, доставкой.
Если клиент хочет заказать — попроси телефон и адрес.
"""

def call_yandex_ai(user_message, conversation_history=None):
    """Вызов YandexGPT через requests"""
    try:
        if not IAM_TOKEN and not API_KEY:
            logger.error("IAM_TOKEN и YANDEX_API_KEY не заданы!")
            return "AI временно недоступен."

        # Определяем заголовки авторизации
        if IAM_TOKEN:
            auth_header = f'Bearer {IAM_TOKEN}'
        else:
            auth_header = f'Api-Key {API_KEY}'

        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json',
            'x-folder-id': YANDEX_CLOUD_FOLDER_ID
        }

        # Формируем промпт с контекстом
        system_prompt = RESTAURANT_CONTEXT

        if conversation_history:
            history_text = "\n".join([
                f"Клиент: {msg['user']}\nКонсультант: {msg['bot']}"
                for msg in conversation_history[-5:]
            ])
            system_prompt += f"\n\nИстория разговора:\n{history_text}"

        messages = [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": user_message}
        ]

        data = {
            "modelUri": MODEL_URI,
            "completionOptions": {
                "temperature": 0.7,
                "maxTokens": 500
            },
            "messages": messages
        }

        response = requests.post(YANDEX_AI_URL, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            return result['result']['alternatives'][0]['message']['text'].strip()
        else:
            logger.error(f"Yandex AI error {response.status_code}: {response.text}")
            return "Произошла ошибка при обработке запроса."
    except Exception as e:
        logger.error(f"Error calling Yandex AI: {str(e)}")
        return "Ошибка соединения с AI."


@app.route('/')
def index():
    """Главная страница — отдаем HTML из корня"""
    try:
        return render_template('lend_version1.html')
    except Exception as e:
        logger.error(f"Template not found: {e}")
        return "<h1 style='color:red'>Ошибка: не найден lend_version1.html</h1>", 500


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
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Chat API error: {str(e)}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


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
        'ai_ready': bool(IAM_TOKEN or API_KEY),
        'version': '1.0'
    })


# === Запуск приложения ===
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    logger.info(f"🚀 Сервер запущен на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
