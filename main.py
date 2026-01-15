import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# ТВОИ КЛЮЧИ
TOKEN = "8586072127:AAGbnc1Y86ZFU-Cl7K9UIUilsfiqzDhnxn4"
GOOGLE_KEY = "AIzaSyBCnKsKlyRGVfYq9nN4Jkmtw1UVfYiegp4"

# Настройка ИИ
genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TOKEN)

# --- ЭТО ДЛЯ RENDER (чтобы не было ошибки портов) ---
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --------------------------------------------------
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Пытаемся получить ответ от ИИ
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Если ИИ упал, бот хотя бы напишет об этом в лог и ответит тебе
        print(f"Ошибка ИИ: {e}")
        bot.reply_to(message, "Я тебя слышу, но у моей нейросети возникла заминка. Попробуй позже!")

if __name__ == "__main__":
    print("Бот запускается...")
    keep_alive() # Запускаем микро-сайт для Render
    bot.infinity_polling()
