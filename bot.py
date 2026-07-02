import os
import subprocess
import sys
import time

# 🚀 डिपेंडेंसी चेक और ऑटो-इंस्टॉल
try:
    import yt_dlp
except ImportError:
    print("📥 yt_dlp is missing! Launching automatic pip installer...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "pyTelegramBotAPI"])
    import yt_dlp

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 आपका Bot Token
BOT_TOKEN = "8986791054:AAE9c01R4YHqXIgDlJQDxbnJm19vS7aNq3A"
bot = telebot.TeleBot(BOT_TOKEN)

# 📥 डायरेक्ट डाउनलोड लिंक जनरेट करने का इंजन (बिना फाइल डाउनलोड किए)
def get_direct_download_link(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best', # बेस्ट क्वालिटी MP4 लिंक
        'username': 'oauth',            # यूट्यूब बॉट ब्लॉकिंग बाईपास
        'cachedir': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False) # download=False यानी सर्वर पर डाउनलोड नहीं होगा, सिर्फ लिंक निकालेगा
        return {
            'title': info.get('title', 'Video'),
            'download_url': info.get('url', None),
            'duration': info.get('duration', 0)
        }

# 🤖 टेलीग्राम /start कमांड
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_msg = (
        "📥 **ONE-CORE UNLIMITED YT DOWNLOADER** 📥\n\n"
        "अब इस बॉट पर **कोई साइज लिमिट नहीं है!** आप 1GB या उससे बड़ी वीडियो भी डाउनलोड कर सकते हैं।\n\n"
        "मुझे किसी भी यूट्यूब वीडियो या शॉर्ट्स का लिंक भेजें, मैं आपको सीधे हाई-स्पीड डाउनलोड लिंक दूंगा।"
    )
    bot.reply_to(message, welcome_msg, parse_mode="Markdown")

# 🔗 लिंक डिटेक्शन और प्रोसेसिंग कोर
@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    url = message.text
    
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = bot.reply_to(message, "⏳ *Extracting direct streaming links from YouTube architecture...*", parse_mode="Markdown")
        
        try:
            # वीडियो का डायरेक्ट लिंक निकालना (यह इंस्टेंट होता है, समय नहीं लेता)
            video_data = get_direct_download_link(url)
            
            if video_data['download_url']:
                # सुंदर इनलाइन बटन बनाना
                markup = InlineKeyboardMarkup()
                download_button = InlineKeyboardButton(text="📥 Download Video (No Size Limit)", url=video_data['download_url'])
                markup.add(download_button)
                
                response_text = (
                    f"🎬 **Title:** {video_data['title']}\n"
                    f"⏱️ **Duration:** {video_data['duration']} seconds\n\n"
                    f"🚀 नीचे दिए गए बटन पर क्लिक करके वीडियो को किसी भी साइज में सीधे डाउनलोड करें:"
                )
                
                # पुराना मैसेज डिलीट करके बटन वाला मैसेज भेजना
                bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
                bot.send_message(message.chat.id, response_text, reply_markup=markup, parse_mode="Markdown")
            else:
                bot.edit_message_text("❌ डायरेक्ट डाउनलोड लिंक जेनरेट नहीं हो पाया।", chat_id=message.chat.id, message_id=status_msg.message_id)
                
        except Exception as e:
            error_text = str(e)
            if "google.com/device" in error_text:
                bot.edit_message_text("⚠️ **Action Required:** Please check GitHub Actions console logs to complete the Google OAuth code verification.", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text("❌ **Error:** लिंक एक्सट्रैक्ट करने में विफल। कृपया सुनिश्चित करें कि लिंक सही है या OAuth वेरीफाइड है।", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ कृपया एक वैलिड यूट्यूब वीडियो का लिंक भेजें।")

if __name__ == "__main__":
    print("🚀 Unlimited Size YT Downloader Engine Started...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"⚠️ Polling dropped, retrying in 5s... Error: {e}")
            time.sleep(5)
