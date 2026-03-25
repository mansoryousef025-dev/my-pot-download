import telebot
import requests

# --- Configuration ---
API_TOKEN = '8737553445:AAEgS4zcfQToFjrDspLiBsE7EecvpU6IacY'
CHANNEL_ID = '@USF'
CHANNEL_LINK = 'https://t.me/usf_0011'

bot = telebot.TeleBot(API_TOKEN)

def check_sub(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        if status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    if not check_sub(message.from_user.id):
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("Join Channel", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, f"Please subscribe to our channel first:\n{CHANNEL_ID}", reply_markup=markup)
        return
    
    bot.reply_to(message, f"عامل اي يا عجل 😘 {user_name}!\n\nSend me any video link (TikTok, Insta, FB, YouTube) to download.")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    if not check_sub(message.from_user.id):
        bot.reply_to(message, f"Access Denied! Please join: {CHANNEL_ID}")
        return

    url = message.text
    if "http" not in url:
        return bot.reply_to(message, "Please send a valid URL!")

    wait_msg = bot.reply_to(message, "Processing... Please wait ⏳")

    try:
        api_url = "https://api.cobalt.tools/api/json"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        data = {"url": url}

        response = requests.post(api_url, json=data, headers=headers)
        result = response.json()

        if "url" in result:
            video_url = result["url"]
            # إرسال الفيديو للمستخدم مع الجملة اللي طلبتها
            bot.send_video(message.chat.id, video_url, caption=f"Downloaded Successfully ✅\n\nاي خدمه يا عجل 😍")
            
            # إرسال نسخة لقناتك للتخزين
            bot.send_video(CHANNEL_ID, video_url, caption=f"New Download 📥\nBy: {message.from_user.first_name}\nSource: {url}")
            
            bot.delete_message(message.chat.id, wait_msg.message_id)
        else:
            bot.edit_message_text("Error: Could not fetch video. Make sure the link is public.", message.chat.id, wait_msg.message_id)

    except Exception as e:
        bot.edit_message_text("Technical Error occurred. Please try again later.", message.chat.id, wait_msg.message_id)

print("Bot is running... Ready for the 'Egl' messages! 😂")
bot.infinity_polling()
