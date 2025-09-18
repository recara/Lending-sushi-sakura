from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
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
FOLDER_ID = os.getenv('YANDEX_CLOUD_FOLDER_ID', 'b1ga94okgf6e5d8edu0u')
API_KEY = os.getenv('YANDEX_API_KEY')  # Лучше назвать переменную понятно

if not API_KEY:
    logger.error("YANDEX_API_KEY не задан!")

try:
    from yandex_cloud_ml_sdk import YCloudML

    # Используем API-ключ напрямую
    sdk = YCloudML(folder_id=FOLDER_ID, auth=API_KEY)

    # Настраиваем модель
    model = sdk.models.completions("yandexgpt-lite", model_version="latest")
    model = model.configure(temperature=0.7, max_tokens=500)

    logger.info("✅ YandexGPT SDK успешно инициализирован с API-ключом")

except Exception as e:
    logger.error(f"❌ Ошибка инициализации SDK: {e}")
    sdk = None
    model = None


def call_yandex_ai(user_message, conversation_history=None):
    """Вызов YandexGPT через SDK"""
    if not model:
        return "Извините, AI временно недоступен."

    try:
        system_prompt = """
Ты - AI-консультант ресторана японской кухни "Sakura Sushi".
Отвечай кратко, дружелюбно, помоги с выбором блюд, доставкой и заказами.
        """.strip()

        messages = [{"role": "system", "text": system_prompt}]

        if conversation_history:
            for msg in conversation_history[-5:]:
                messages.append({"role": "user", "text": msg["user"]})
                messages.append({"role": "bot", "text": msg["bot"]})

        messages.append({"role": "user", "text": user_message})

        result = model.run(messages)

        if result.is_failed():
            logger.error(f"AI failed: {result.error}")
            return "Произошла ошибка при генерации ответа."

        return str(result)

    except Exception as e:
        logger.error(f"Error calling Yandex AI: {str(e)}")
        return "Извините, произошла техническая ошибка."


@app.route('/')
def index():
    try:
        return render_template('lend_version1.html')
    except Exception as e:
        logger.error(f"Template error: {e}")
        return "<h1>Ошибка: шаблон не найден</h1>", 500


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        history = data.get('history', [])

        if not user_message:
            return jsonify({'error': 'Пустое сообщение'}), 400

        ai_response = call_yandex_ai(user_message, history)
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': 'Ошибка сервера'}), 500


@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'sdk_ready': model is not None,
        'api_key_set': bool(API_KEY),
        'version': '1.0'
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
