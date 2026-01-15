import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# ТВОИ КЛЮЧИ
TOKEN = "8580398532:AAF6s9uYzV8eq-YO5h8vsHgypl_f00oONNY"
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
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка ИИ: {e}")

if __name__ == "__main__":
    print("Бот запускается...")
    keep_alive() # Запускаем микро-сайт для Render
    bot.infinity_polling()
