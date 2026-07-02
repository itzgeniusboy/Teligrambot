import os
import subprocess
import sys

# 🚀 [SUPER HACK] अगर yt_dlp इंस्टॉल नहीं है, तो यह स्क्रिप्ट खुद उसे इंस्टॉल कर लेगी
try:
    import yt_dlp
except ImportError:
    print("📥 yt_dlp missing! Installing via fallback architecture...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "pyTelegramBotAPI"])
    import yt_dlp

import telebot

# 🔑 आपका Bot Token
BOT_TOKEN = "8986791054:AAE9c01R4YHqXIgDlJQDxbnJm19vS7aNq3A"
bot = telebot.TeleBot(BOT_TOKEN)

# --- पुराना बाकी का पूरा कोड यहाँ पेस्ट कर दें ---
def download_yt_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'max_filesize': 45 * 1024 * 1024,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "📥 **YT DOWNLOADER LIVE** 📥\n\nमुझे लिंक भेजो, मैं डाउनलोड कर दूंगा!", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = bot.reply_to(message, "⏳ *Processing video...*", parse_mode="Markdown")
        try:
            video_file = download_yt_video(url)
            bot.edit_message_text("🚀 *Uploading to Telegram...*", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove(video_file)
            bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ **Error:** {str(e)}", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    print("🚀 YT Downloader Engine Started...")
    bot.infinity_polling()
