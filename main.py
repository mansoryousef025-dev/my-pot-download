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
        btn = telebot.types.InlineKeyboardButton("Join Channel | اشترك هنا", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, f"اشترك في القناة أولاً يا عجل:\n{CHANNEL_ID}", reply_markup=markup)
        return
    bot.reply_to(message, f"عامل اي يا عجل 😘 {user_name}!\n\nابعت اللينك يا عجل وهنزلهولك فوراً.")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    if not check_sub(message.from_user.id):
        bot.reply_to(message, f"اشترك في القناة الأول يا عجل: {CHANNEL_ID}")
        return

    url = message.text
    if "http" not in url:
        return bot.reply_to(message, "اللينك غلط يا عجل!")

    wait_msg = bot.reply_to(message, "جاري التحميل... ثواني يا عجل ⏳")

    try:
        # Try Server 1: Cobalt API
        api_url = "https://api.cobalt.tools/api/json"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        data = {"url": url, "vCodec": "h264"}
        
        response = requests.post(api_url, json=data, headers=headers)
        result = response.json()

        if "url" in result:
            bot.send_video(message.chat.id, result["url"], caption="اي خدمه يا عجل 😍")
            bot.delete_message(message.chat.id, wait_msg.message_id)
            return

        # Try Server 2: TiklyDown (Fallback)
        alt_res = requests.get(f"https://api.tiklydown.eu.org/api/download?url={url}").json()
        if "data" in alt_res and "video" in alt_res["data"]:
            bot.send_video(message.chat.id, alt_res["data"]["video"]["noWatermark"], caption="اي خدمه يا عجل 😍")
            bot.delete_message(message.chat.id, wait_msg.message_id)
            return
            
        bot.edit_message_text("السيرفر مشغول يا عجل، جرب لينك تاني ❌", message.chat.id, wait_msg.message_id)

    except:
        bot.edit_message_text("حصل خطأ فني يا عجل، جرب كمان شوية 🛠️", message.chat.id, wait_msg.message_id)

bot.infinity_polling()
