import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- НАСТРОЙКИ (КЛЮЧИ) ---
# Актуальный токен из BotFather (начинается на 8586...)
BOT_TOKEN = "8586072127:AAE9tfgdgyBcIHd3T9tCF3bCp5SbC-GyTfA"

# Твой API-ключ Gemini (начинается на AIza...)
GOOGLE_KEY = "AIzaSyDnyckWdUCI_sVGwx3uqX-tNCVJ92_p8jg"

# Настройка ИИ (используем стабильную версию 1.5-flash)
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
        # Выводим точную ошибку в логи Render
        print(f"ОШИБКА GEMINI: {e}")
        bot.reply_to(message, "Я тебя слышу, но у моей нейросети возникла заминка. Попробуй еще раз!")

# --- ЗАПУСК ---
if __name__ == "__main__":
    print("--- ЗАПУСК БОТА ---")
    keep_alive()  # Запускаем веб-сервер
    
    # ЭТА СТРОЧКА УБИРАЕТ ОШИБКУ 409
    bot.remove_webhook()
    
    try:
        print("Бот готов к работе!")
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
