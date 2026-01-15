import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# --- НАСТРОЙКИ ---
BOT_TOKEN = "8586072127:AAE9tfgdgyBcIHd3T9tCF3bCp5SbC-GyTfA"
GOOGLE_KEY = "AIzaSyDnyckWdUCI_sVGwx3uqX-tNCVJ92_p8jg"

# Инициализация ИИ
genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# --- ВЕБ-СЕРВЕР ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Render автоматически подставит нужный порт
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True # Поток завершится вместе с основной программой
    t.start()

# --- ОБРАБОТКА СООБЩЕНИЙ ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Система перезапущена! Теперь я готов отвечать.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        bot.reply_to(message, "Произошла ошибка в нейросети. Попробуйте ещё раз через минуту.")

# --- ГЛАВНЫЙ ЗАПУСК ---
if __name__ == "__main__":
    print("--- ЗАПУСК СИСТЕМЫ ---")
    keep_alive() 
    
    # КЛЮЧЕВОЕ РЕШЕНИЕ:
    # 1. Принудительно отключаем любые вебхуки
    bot.remove_webhook()
    time.sleep(1) # Короткая пауза для синхронизации с серверами Telegram
    
    print("Бот успешно подключен. Ожидаю сообщений...")
    
    # Запуск опроса с защитой от ошибок
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
