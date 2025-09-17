#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API Sakura Sushi
"""

import requests
import json
import time

# Конфигурация
BASE_URL = "http://localhost:5000"  # Измените на ваш URL

def test_health_check():
    """Тест health check endpoint"""
    print("🔍 Тестирование health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_chat_api():
    """Тест chat API"""
    print("\n💬 Тестирование chat API...")
    
    test_messages = [
        "Привет! Что у вас есть?",
        "Рекомендуйте роллы",
        "Сколько стоит доставка?",
        "Хочу заказать Филадельфию"
    ]
    
    for message in test_messages:
        try:
            print(f"📤 Отправка: {message}")
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json={
                    "message": message,
                    "history": []
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"📥 Ответ: {data['response']}")
            else:
                print(f"❌ Ошибка: {response.status_code} - {response.text}")
            
            time.sleep(1)  # Пауза между запросами
            
        except Exception as e:
            print(f"❌ Ошибка запроса: {e}")

def test_menu_api():
    """Тест menu API"""
    print("\n🍣 Тестирование menu API...")
    try:
        response = requests.get(f"{BASE_URL}/api/menu")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Menu API OK: {len(data['menu'])} блюд")
            for item in data['menu'][:3]:  # Показываем первые 3
                print(f"  - {item['name']}: {item['price']} ₽")
        else:
            print(f"❌ Menu API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Menu API error: {e}")

def test_order_api():
    """Тест order API"""
    print("\n📦 Тестирование order API...")
    
    test_order = {
        "name": "Тестовый Клиент",
        "phone": "+79123456789",
        "email": "test@example.com",
        "address": "г. Владивосток, ул. Тестовая, 1",
        "delivery_time": "asap",
        "payment_method": "cash",
        "comment": "Тестовый заказ",
        "items": [
            {
                "title": "Филадельфия",
                "price": 490,
                "quantity": 1
            }
        ],
        "total": 490
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/order",
            json=test_order,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Order API OK: {data}")
        else:
            print(f"❌ Order API failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Order API error: {e}")

def test_main_page():
    """Тест главной страницы"""
    print("\n🏠 Тестирование главной страницы...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            if "Sakura Sushi" in response.text:
                print("✅ Главная страница загружается корректно")
            else:
                print("⚠️ Главная страница загружается, но контент не найден")
        else:
            print(f"❌ Главная страница failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Главная страница error: {e}")

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов Sakura Sushi API")
    print(f"📍 URL: {BASE_URL}")
    print("=" * 50)
    
    # Запускаем тесты
    tests = [
        test_health_check,
        test_main_page,
        test_menu_api,
        test_chat_api,
        test_order_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except:
            pass
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно!")
    else:
        print("⚠️ Некоторые тесты не прошли. Проверьте конфигурацию.")

if __name__ == "__main__":
    main()
