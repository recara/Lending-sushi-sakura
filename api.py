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
IAM_TOKEN = os.getenv('IAM_TOKEN')  # Обязательно задайте в Render!
MODEL_URI = f"gpt://{YANDEX_CLOUD_FOLDER_ID}/yandexgpt-lite/latest"
YANDEX_AI_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

# === Контекст AI ===
RESTAURANT_CONTEXT = """
Ты — AI‑консультант ресторана японской кухни "Sakura Sushi" (г. Владивосток).
Говори кратко и по делу, дружелюбно. Предлагай блюда, помогай с доставкой и оформлением заказа.

Актуальные разделы меню (категории фильтра):
- Все, Роллы, Супы, Лапша, Горячее, Сашими, Суши, Салаты, Десерты, Напитки, Закуски.

Популярные позиции и цены (ориентируйся на них при ответах):
- Роллы: «Филадельфия» — 490 ₽, «Калифорния» — 450 ₽, «Дракон» — 620 ₽, сет «Самурай» — 1390 ₽, «Темпура ролл» — 520 ₽, «Чиз ролл» — 410 ₽.
- Супы: «Мисо суп» — 190 ₽, «Том Ям» — 490 ₽.
- Лапша/горячее: «Рамен» — 450 ₽, «Удон с курицей» — 390 ₽, «Гёдза» — 320 ₽, «Говядина булгоги» — 620 ₽.
- Сашими/суши: «Сашими» ассорти — 560 ₽, «Суши с креветкой» — 120 ₽.
- Салаты: «Салат Чука» — 270 ₽, «Салат из водорослей» — 220 ₽.
- Десерты: «Моти/Мочи» — 280 ₽, «Чизкейк» — 320 ₽.
- Напитки: «Зелёный чай» — 150 ₽, «Рамунэ» — 180 ₽, «Саке» — 350 ₽.
- Закуски: «Эби темпура» — 280 ₽, «Картофель фри» — 180 ₽.

Условия доставки (со страницы):
- Зона: в пределах КАД и до 5 км за КАД.
- Сроки: 45 мин будни, 60 мин выходные.
- Минимальная сумма заказа: 900 ₽.
- Доставка: бесплатно от 1500 ₽, иначе 150 ₽.

Как оформлять заказ: попроси телефон и адрес в формате «+7ХХХХХХХХХХ, город, улица, дом»,
предложи выбрать блюда из категорий выше. Если пользователь просит рекомендацию — предложи 2–3 популярных
варианта из соответствующей категории с ценами. Если спрашивают позицию, которой нет в списках,
скажи, что её сейчас нет в наличии и предложи близкие альтернативы.

Стиль: 1–3 коротких предложения, без лишней воды. Если нужен следующий шаг — явно спроси.
"""

def call_yandex_ai(user_message, conversation_history=None):
    """Вызов YandexGPT Lite"""
    try:
        if not IAM_TOKEN:
            logger.error("IAM_TOKEN не задан!")
            return "AI временно недоступен. Попробуйте позже."

        headers = {
            'Authorization': f'Bearer {IAM_TOKEN}',
            'Content-Type': 'application/json',
            'x-folder-id': YANDEX_CLOUD_FOLDER_ID
        }

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
        logger.error(f"AI Error: {str(e)}")
        return "Ошибка соединения с AI."


@app.route('/')
def index():
    """Главная страница"""
    try:
        return render_template('lend_version1.html')
    except Exception as e:
        logger.error(f"Template error: {e}")
        return "<h1>Ошибка: шаблон не найден</h1>", 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Чат с AI"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        history = data.get('history', [])

        if not user_message:
            return jsonify({'error': 'Сообщение пустое'}), 400

        ai_response = call_yandex_ai(user_message, history)
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': 'Ошибка сервера'}), 500


@app.route('/api/menu', methods=['GET'])
def get_menu():
    """Меню"""
    menu = [
        {"id": 1, "name": "Филадельфия", "price": 490, "category": "rolls"},
        {"id": 2, "name": "Сет Самурай", "price": 1390, "category": "rolls"},
        {"id": 3, "name": "Рамен", "price": 450, "category": "noodles"},
        {"id": 4, "name": "Мисо суп", "price": 190, "category": "soups"},
        {"id": 5, "name": "Сашими", "price": 560, "category": "sashimi"}
    ]
    return jsonify({'menu': menu})


@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'ai_ready': bool(IAM_TOKEN)
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
