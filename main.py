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

    # المحاولة الوحيدة المضمونة (سيرفر Cobalt الأصلي)
    try:
        payload = {
            "url": url,
            "vCodec": "h264", # عشان يشتغل على كل الموبايلات
            "videoQuality": "720",
            "isNoWatermark": True
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # السيرفر ده هو اللي شغال نار دلوقتي
        res = requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers)
        data = res.json()

        if "url" in data:
            bot.send_video(message.chat.id, data["url"], caption="اي خدمه يا عجل 😍")
            bot.delete_message(message.chat.id, wait_msg.message_id)
        elif "picker" in data:
            # لو اللينك صور (زي تيك توك صور)
            for item in data["picker"]:
                bot.send_photo(message.chat.id, item["url"])
            bot.delete_message(message.chat.id, wait_msg.message_id)
        else:
            bot.edit_message_text("السيرفر بيقولك اللينك ده تقيل عليه يا عجل، جرب فيديو تاني ❌", message.chat.id, wait_msg.message_id)

    except Exception as e:
        bot.edit_message_text("في ضغط كبير يا عجل، جرب كمان شوية 🛠️", message.chat.id, wait_msg.message_id)

bot.infinity_polling()
