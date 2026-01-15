import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- НАСТРОЙКИ ---
# Твой актуальный токен и ключ Gemini
BOT_TOKEN = "8586072127:AAE9tfgdgyBcIHd3T9tCF3bCp5SbC-GyTfA"
GOOGLE_KEY = "AIzaSyDnyckWdUCI_sVGwx3uqX-tNCVJ92_p8jg"

# Настройка Gemini
genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Настройка Telegram бота
bot = telebot.TeleBot(BOT_TOKEN)

# --- ВЕБ-СЕРВЕР (ДЛЯ ПОРТА RENDER) ---
app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run():
    # Render передает порт через переменную окружения, либо используем 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- ЛОГИКА БОТА ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Я полностью перезапущен и готов к работе!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка Gemini: {e}")
        bot.reply_to(message, "Я тебя слышу, но нейросеть задумалась. Попробуй еще раз!")

# --- ЗАПУСК ---
if __name__ == "__main__":
    print("--- СИСТЕМА ЗАПУСКАЕТСЯ ---")
    keep_alive() # Запуск Flask в отдельном потоке
    
    # КЛЮЧЕВОЙ МОМЕНТ: Удаляем старые вебхуки, чтобы убрать ошибку 409
    bot.remove_webhook()
    
    print("Соединение с Telegram установлено. Жду сообщений...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
