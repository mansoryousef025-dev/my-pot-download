import telebot
import yt_dlp
import os

# حط بياناتك هنا بحرص
TOKEN = '8737553445:AAGwi84SeVsoy9W08bmtftI45eOWpsleHj4'
CHANNEL_ID = '@usf_0011'
CHANNEL_URL = 'https://t.me/usf_0011'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        # فحص الاشتراك
        status = bot.get_chat_member(CHANNEL_ID, m.from_user.id).status
        if status not in ['member', 'administrator', 'creator']:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton("اشترك هنا ✅", url=CHANNEL_URL))
            return bot.send_message(m.chat.id, "اشترك الأول يا بطل 👇", reply_markup=markup)
        
        # التحميل
        url = m.text
        if 'http' in url:
            bot.reply_to(m, "جاري التحميل... ⏳")
            ydl_opts = {'outtmpl': 'v.mp4', 'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open('v.mp4', 'rb') as v:
                bot.send_video(m.chat.id, v)
            os.remove('v.mp4')
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(m, "فيه مشكلة، ابعت رابط تاني أو اشترك في القناة!")

bot.polling(none_stop=True)
