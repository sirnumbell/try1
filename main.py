import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- НАСТРОЙКИ ---
# Вставь сюда свои актуальные ключи
BOT_TOKEN = "8121652758:AAGS46Ea93p_hY879A5SbC-GyTfA"
GOOGLE_KEY = "AIzaSyDnyckWdUcI_sVGwx3uqX-tNCVJ92_p8jg" # Убедись, что здесь твой новый ключ Gemini

# Настройка Gemini
genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-pro')

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
    bot.reply_to(message, "Привет! Я твой ИИ-помощник. Напиши мне любой вопрос.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Отправляем текст в нейросеть
        response = model.generate_content(message.text)
        # Отвечаем пользователю результатом
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        bot.reply_to(message, "Я тебя слышу, но у моей нейросети возникла заминка. Попробуй еще раз через минуту!")

# --- ЗАПУСК ---
if __name__ == "__main__":
    print("Запуск бота...")
    keep_alive()  # Запускаем веб-сервер
    
    # Очистка старых соединений перед стартом
    bot.remove_webhook()
    
    # Запуск бесконечного цикла с защитой от вылета
    try:
        bot.polling(none_stop=True, interval=1, timeout=20)
    except Exception as e:
        print(f"Ошибка при работе: {e}")
