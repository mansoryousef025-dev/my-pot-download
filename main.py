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
        # السيرفر ده (SaveFrom البديل) بيسحب تقريباً كل المواقع
        api_url = f"https://api.vkrdown.com/api/download?url={url}"
        response = requests.get(api_url).json()

        if "data" in response and "url" in response["data"]:
            video_url = response["data"]["url"]
            bot.send_video(message.chat.id, video_url, caption="اي خدمه يا عجل 😍")
            bot.delete_message(message.chat.id, wait_msg.message_id)
        else:
            # محاولة أخيرة بسيرفر تيك توك مخصوص لو اللينك تيك توك
            alt_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
            alt_res = requests.get(alt_url).json()
            if "data" in alt_res and "video" in alt_res["data"]:
                bot.send_video(message.chat.id, alt_res["data"]["video"]["noWatermark"], caption="اي خدمه يا عجل 😍")
                bot.delete_message(message.chat.id, wait_msg.message_id)
            else:
                bot.edit_message_text("اللينك ده تقيل ع السيرفر يا عجل، جرب لينك تاني ❌", message.chat.id, wait_msg.message_id)

    except Exception:
        bot.edit_message_text("حصل قفلة في السيرفر يا عجل، جرب كمان دقيقة 🛠️", message.chat.id, wait_msg.message_id)

bot.infinity_polling()
