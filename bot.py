import os
import telebot
import yt_dlp

BOT_TOKEN = "8986791054:AAE9c01R4YHqXIgDlJQDxbnJm19vS7aNq3A"
bot = telebot.TeleBot(BOT_TOKEN)

# वीडियो डाउनलोड करने का फंक्शन
def download_yt_video(url):
    # सिर्फ वो वीडियो डाउनलोड करेंगे जो 50MB से छोटी हो (टेलीग्राम बॉट लिमिट के कारण)
    ydl_opts = {
        'format': 'best[ext=mp4]/best', # बेस्ट MP4 क्वालिटी
        'outtmpl': 'downloads/%(title)s.%(ext)s', # डाउनलोड फोल्डर में सेव होगा
        'max_filesize': 45 * 1024 * 1024, # 45MB की लिमिट ताकि टेलीग्राम पर सेंड हो सके
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "📥 **ONE-CORE YT DOWNLOADER** 📥\n\nमुझे किसी भी यूट्यूब वीडियो का लिंक भेजो, मैं उसे डाउनलोड करके तुम्हें भेज दूंगा!\n*(नोट: वीडियो 50MB से कम की होनी चाहिए)*", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    url = message.text
    
    if "youtube.com" in url or "youtu.be" in url or "youtube.com/shorts" in url:
        status_msg = bot.reply_to(message, "⏳ *Processing video link, fetching buffers...*", parse_mode="Markdown")
        
        try:
            # वीडियो डाउनलोड शुरू
            bot.edit_message_text("📥 *Downloading video from YouTube infrastructure...*", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
            video_file = download_yt_video(url)
            
            # टेलीग्राम पर वीडियो सेंड करना
            bot.edit_message_text("🚀 *Uploading video to Telegram clouds...*", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
            
            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="🔥 Downloaded via Your Platform")
            
            # क्लीनअप: अपलोड के बाद सर्वर से वीडियो डिलीट करना ताकि स्पेस न भरे
            os.remove(video_file)
            bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)
            
        except Exception as e:
            bot.edit_message_text(f"❌ **Error:** {str(e)}\n*(शायद वीडियो 50MB से बड़ी है या लिंक इनवैलिड है)*", chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ कृपया एक वैलिड यूट्यूब वीडियो या शॉर्ट्स का लिंक भेजें।")

if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    print("🚀 YT Downloader Engine Started...")
    bot.infinity_polling()
