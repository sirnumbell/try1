Конечно! Давай сделаем так: я дам тебе полный, финальный текст кода, где уже заменены названия моделей на самые стабильные и добавлены все нужные исправления.

Тебе нужно просто стереть всё в твоем файле main.py на GitHub и вставить этот текст целиком.

Python

import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- 1. НАСТРОЙКИ (КЛЮЧИ) ---
# Твой новый токен от BotFather (который начинается на 8586...)
BOT_TOKEN = "8586072127:AAGS46Ea93p_hY879A5SbC-GyTfA"

# Твой API-ключ от Google AI Studio (который начинается на AIza...)
GOOGLE_KEY = "AIzaSyDnyckWdUCI_sVGwx3uqX-tNCVJ92_p8jg"

# Настройка нейросети
genai.configure(api_key=GOOGLE_KEY)
# Используем модель 1.5-flash — она самая быстрая и надежная для бесплатных аккаунтов
model = genai.GenerativeModel('gemini-1.5-flash')

# Настройка Telegram бота
bot = telebot.TeleBot(BOT_TOKEN)

# --- 2. ВЕБ-СЕРВЕР ДЛЯ RENDER (ЧТОБЫ БОТ НЕ СПАЛ) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 3. ЛОГИКА ОБРАБОТКИ СООБЩЕНИЙ ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой ИИ-помощник на базе Gemini. Напиши мне любой вопрос, и я постараюсь ответить!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Отправляем текст пользователя в Gemini
        response = model.generate_content(message.text)
        
        # Если ответ пустой или заблокирован фильтрами
        if not response.text:
            bot.reply_to(message, "Извини, я не могу ответить на этот вопрос.")
        else:
            bot.reply_to(message, response.text)
            
    except Exception as e:
        # Выводим ошибку в логи Render, чтобы мы могли её увидеть
        print(f"ОШИБКА GEMINI: {e}")
        bot.reply_to(message, "Я тебя слышу, но у моей нейросети возникла заминка. Попробуй задать вопрос еще раз через минуту!")

# --- 4. ЗАПУСК БОТА ---
if __name__ == "__main__":
    print("--- БОТ ЗАПУСКАЕТСЯ ---")
    keep_alive()  # Запуск веб-сервера
    
    # Сброс старых подключений (защита от ошибки 409)
    bot.remove_webhook()
    
    # Запуск бота в режиме бесконечного опроса
    try:
        print("Бот успешно подключен к Telegram и ждет сообщений...")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Критическая ошибка запуска: {e}")
