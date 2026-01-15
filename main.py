import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- НАСТРОЙКИ (КЛЮЧИ) ---
# Токен из твоего скриншота BotFather (заканчивается на GyTfA)
BOT_TOKEN = "8586072127:AAE9tfgdgyBcIHd3T9tCF3bCp5SbC-GyTfA"

# Ключ из твоего скриншота Google AI Studio (начинается на AIzaSyD)
GOOGLE_KEY = "AIzaSyDnyckWdUCI_sVGwx3uqX-tNCVJ92_p8jg"

# Настройка нейросети (используем стабильную версию 1.5-flash)
genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Настройка Telegram бота
bot = telebot.TeleBot(BOT_TOKEN)

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- ЛОГИКА БОТА ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой ИИ-помощник. Напиши мне любой вопрос!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Отправляем текст в нейросеть
        response = model.generate_content(message.text)
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Извини, я не смог сформировать ответ.")
    except Exception as e:
        # Пишем ошибку в логи Render для диагностики
        print(f"ОШИБКА GEMINI: {e}")
        bot.reply_to(message, "Я тебя слышу, но у моей нейросети возникла заминка. Попробуй еще раз через минуту!")

# --- ЗАПУСК ---
if __name__ == "__main__":
    print("--- ЗАПУСК БОТА ---")
    keep_alive()  # Запускаем веб-сервер
    
    # Сброс старых подключений (защита от ошибки 409)
    bot.remove_webhook()
    
    try:
        print("Бот успешно запущен и ждет сообщений...")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
