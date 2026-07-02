import os
import subprocess
import sys
import time

# 🚀 [STEP 1] डिपेंडेंसी चेक और ऑटो-इंस्टॉल आर्किटेक्चर
try:
    import yt_dlp
except ImportError:
    print("📥 yt_dlp is missing! Launching automatic pip installer...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "pyTelegramBotAPI"])
    import yt_dlp

import telebot

# 🔑 आपका BotFather वाला टोकन (यह पहले से ही सही सेट है)
BOT_TOKEN = "8986791054:AAE9c01R4YHqXIgDlJQDxbnJm19vS7aNq3A"
bot = telebot.TeleBot(BOT_TOKEN)

# 📥 यूट्यूब वीडियो डाउनलोडर इंजन (OAuth बाईपास के साथ)
def download_yt_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best', # बेस्ट MP4 वीडियो क्वालिटी
        'outtmpl': 'downloads/%(title)s.%(ext)s', # डाउनलोड पाथ
        'max_filesize': 48 * 1024 * 1024, # 48MB लिमिट ताकि टेलीग्राम पर अपलोड हो सके
        
        # 🔥 [CRITICAL FIX] यूट्यूब बॉट डिटेक्शन/साइन-इन एरर बाईपास
        'username': 'oauth', 
        'cachedir': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# 🤖 टेलीग्राम /start कमांड हैंडलर
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_msg = (
        "📥 **ONE-CORE YT DOWNLOADER ENGINE** 📥\n\n"
        "मुझे किसी भी यूट्यूब वीडियो या शॉर्ट्स का लिंक भेजें।\n"
        "मैं उसे डाउनलोड करके सीधे यहाँ सेंड कर दूँगा!\n\n"
        "⚠️ *नोट: टेलीग्राम लिमिट के कारण वीडियो 50MB से छोटी होनी चाहिए।*"
    )
    bot.reply_to(message, welcome_msg, parse_mode="Markdown")

# 🔗 लिंक डिटेक्शन और प्रोसेसिंग कोर
@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    url = message.text
    
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = bot.reply_to(message, "⏳ *Processing server buffers, establishing handshake...*", parse_mode="Markdown")
        
        try:
            # स्टेप 1: डाउनलोडिंग शुरू
            bot.edit_message_text("📥 *Downloading file from YouTube infrastructure...*", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
            video_file = download_yt_video(url)
            
            # स्टेप 2: टेलीग्राम पर अपलोडिंग शुरू
            bot.edit_message_text("🚀 *Uploading data packets to Telegram clouds...*", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
            
            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="🔥 Downloaded via Your Platform")
            
            # स्टेप 3: स्टोरेज क्लीनअप (फाइल डिलीट करना ताकि स्पेस न भरे)
            if os.path.exists(video_file):
                os.remove(video_file)
                
            bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
            
        except Exception as e:
            error_text = str(e)
            # अगर पहली बार OAuth का कोड टर्मिनल में प्रिंट हो रहा है
            if "google.com/device" in error_text:
                bot.edit_message_text("⚠️ **Action Required:** Please check GitHub Actions console logs to complete the Google OAuth code verification.", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text(f"❌ **Error:** Video downloading failed.\n*(शायद फाइल 50MB से बड़ी है या यूट्यूब ने ब्लॉक किया है)*", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ कृपया एक वैलिड यूट्यूब वीडियो या शॉर्ट्स का लिंक भेजें।")

if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    print("🚀 Advanced YT Downloader Engine Started...")
    
    # एंटी-क्रैश पोलिंग लूप
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"⚠️ Polling connection dropped, retrying in 5s... Error: {e}")
            time.sleep(5)
