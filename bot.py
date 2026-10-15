import os
import telebot
import requests
from flask import Flask
from threading import Thread

BOT_TOKEN = "8808744495:AAFEg1gNT7nklWeiN0CyxGm-Fr8szSqQ9wU"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("📋 Как получить ключ", callback_data="help_key")
    btn2 = telebot.types.InlineKeyboardButton("🔥 Наши скрипты", callback_data="scripts")
    markup.add(btn1, btn2)
    
    bot.send_message(
        message.chat.id,
        "⚡ **Привет! Это официальный бот SAHUR KEY.**\n\n"
        "Отправь мне ссылку на ключ Delta прямо в чат, и я попробую её обойти!",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "help_key":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "💡 Просто скопируй ссылку на ключ из Delta и отправь её сюда сообщением.")
    elif call.data == "scripts":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📜 Скоро здесь появятся лучшие скрипты для Roblox!")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    
    if not url.startswith("http://") and not url.startswith("https://"):
        bot.reply_to(message, "❌ Отправь корректную ссылку, начинающуюся с `https://`", parse_mode="Markdown")
        return

    status_msg = bot.reply_to(message, "🔄 **Обхожу ссылку, подожди пару секунд...**", parse_mode="Markdown")

    # Альтернативный публичный эндпоинт
    api_endpoint = f"https://api.bypass.city/bypass?url={url}"

    try:
        response = requests.get(api_endpoint, timeout=15).json()

        if response.get("status") == "success" or "result" in response:
            result = response.get("result") or response.get("key")
            bot.edit_message_text(
                f"✅ **Успешный обход!**\n\nТвой ключ/результат:\n`{result}`",
                chat_id=status_msg.chat.id,
                message_id=status_msg.message_id,
                parse_mode="Markdown"
            )
        else:
            bot.edit_message_text(
                "⚠️ Этот метод сейчас обновляется. Скоро подключим новый рабочий сервер!",
                chat_id=status_msg.chat.id,
                message_id=status_msg.message_id
            )
    except Exception:
        bot.edit_message_text(
            "⚠️ Ошибка запроса. Сервер временно перегружен, попробуй еще раз через минуту.",
            chat_id=status_msg.chat.id,
            message_id=status_msg.message_id
        )

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    print("Бот SahurBypass успешно запущен!")
    bot.infinity_polling()
