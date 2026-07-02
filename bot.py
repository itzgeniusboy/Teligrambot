import os
import telebot
import requests

# 🔑 आपका BotFather वाला लाइव टोकन यहाँ डाल दिया है
BOT_TOKEN = "8986791054:AAE9c01R4YHqXIgDlJQDxbnJm19vS7aNq3A"
bot = telebot.TeleBot(BOT_TOKEN)

# 🎯 जिस वेबसाइट को चेक करना है उसका URL यहाँ डालो
TARGET_URL = "https://your-site-link.com" 

def get_site_status(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return f"✅ SITE IS LIVE: Status {response.status_code}"
        else:
            return f"⚠️ SITE ERROR: Status {response.status_code}"
    except Exception as e:
        return f"❌ SITE DOWN: {e}"

# 🤖 /start कमांड का रिप्लाई
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔥 Engine Active! Your multi-bot setup is working perfectly.\nUse /check to verify site status.")

# 🔄 /check कमांड का रिप्लाई
@bot.message_handler(commands=['check'])
def check_status(message):
    bot.reply_to(message, "🔄 Checking site status...")
    report = get_site_status(TARGET_URL)
    bot.reply_to(message, report)

if __name__ == "__main__":
    print("🚀 Polling started...")
    bot.infinity_polling()
