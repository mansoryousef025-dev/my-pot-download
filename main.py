import telebot
import requests

# --- Configuration ---
API_TOKEN = '8737553445:AAEgS4zcfQToFjrDspLiBsE7EecvpU6IacY'
CHANNEL_ID = '@usf_0011'
CHANNEL_LINK = 'https://t.me/usf_0011'

bot = telebot.TeleBot(API_TOKEN)

def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
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
        bot.send_message(message.chat.id, f"Join first:\n{CHANNEL_ID}", reply_markup=markup)
        return
    bot.reply_to(message, f" 😘 عامل اي يا عجل' {user_name}!\n\nSend link to download.")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    if not check_sub(message.from_user.id):
        bot.reply_to(message, f"Join first: {CHANNEL_ID}")
        return

    url = message.text
    if "http" not in url:
        return bot.reply_to(message, "Invalid URL!")

    wait_msg = bot.reply_to(message, "Processing... ⏳")

    try:
        # High speed API for TikTok/Social
        api_url = "https://api.cobalt.tools/api/json"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        payload = {"url": url, "vCodec": "h264"}
        
        response = requests.post(api_url, json=payload, headers=headers)
        result = response.json()

        if "url" in result:
            video_url = result["url"]
            bot.send_video(message.chat.id, video_url, caption="Any service 'عجل' 😍")
            bot.send_video(CHANNEL_ID, video_url, caption=f"Downloaded by: {message.from_user.first_name}")
            bot.delete_message(message.chat.id, wait_msg.message_id)
        else:
            bot.edit_message_text("Error: Fetch failed. Try another link.", message.chat.id, wait_msg.message_id)

    except Exception as e:
        bot.edit_message_text("Technical error. Try again later.", message.chat.id, wait_msg.message_id)

bot.infinity_polling()
