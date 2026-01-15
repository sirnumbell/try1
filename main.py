import os
import telebot
import google.generativeai as genai

# ПРЯМО СЮДА ВСТАВЬ СВОИ КЛЮЧИ В КАВЫЧКАХ
TOKEN = "8059287446:AAGh2wIlfN-ba_-VOw9d587XIj8jBt9NG7M"
GOOGLE_KEY = "AIzaSyBCnKsKlyRGVfYq9nN4Jkmtw1UVfYiegp4"

genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")

print("Bot is running...")
bot.infinity_polling()
bot.infinity_polling()
