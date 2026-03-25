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

    # الخطة (أ): سيرفر VKR (الأسرع حالياً)
    try:
        res = requests.get(f"https://api.vkrdown.com/api/download?url={url}").json()
        if "data" in res and "url" in res["data"]:
            bot.send_video(message.chat.id, res["data"]["url"], caption="اي خدمه يا عجل 😍")
            bot.delete_message(message.chat.id, wait_msg.message_id)
            return
    except: pass

    # الخطة (ب): سيرفر TiklyDown (للتيك توك مخصوص)
    try:
        res = requests.get(f"https://api.tiklydown.eu.org/api/download?url={url}").json()
        if "data" in res and "video" in res["data"]:
            bot.send_video(message.chat.id, res["data"]["video"]["noWatermark"], caption="اي خدمه يا عجل 😍")
            bot.delete_message(message.chat.id, wait_msg.message_id)
            return
    except: pass

    # الخطة (ج): سيرفر Cobalt (لليوتيوب والإنستا)
    try:
        res = requests.post("https://api.cobalt.tools/api/json", 
                            json={"url": url, "vCodec": "h264"}, 
                            headers={"Accept": "application/json"}).json()
        if "url" in res:
            bot.send_video(message.chat.id, res["url"], caption="اي خدمه يا عجل 😍")
            bot.delete_message(message.chat.id, wait_msg.message_id)
            return
    except: pass

    # الخطة (د): سيرفر Loov (احتياطي الأزمات)
    try:
        res = requests.get(f"https://api.loov.io/api/json?url={url}").json()
        if "url" in res:
            bot.send_video(message.chat.id, res["url"], caption="اي خدمه يا عجل 😍")
            bot.delete_message(message.chat.id, wait_msg.message_id)
            return
    except: pass

    # لو كل المحاولات فشلت
    bot.edit_message_text("السيرفرات كلها مهنجة يا عجل، جرب لينك تاني أو فيديو أقصر ❌", message.chat.id, wait_msg.message_id)

bot.infinity_polling()
