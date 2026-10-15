import telebot
import requests

BOT_TOKEN = "8808744495:AAFEg1gNT7nklWeiN0CyxGm-Fr8szSqQ9wU"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 **Привет! Я Sahur Bypass Bot.**\n\nОтправь мне ссылку на ключ Delta, и я мгновенно получу ключ!", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    
    if not url.startswith("http://") and not url.startswith("https://"):
        bot.reply_to(message, "❌ Отправь корректную ссылку, начинающуюся с `https://`", parse_mode="Markdown")
        return

    status_msg = bot.reply_to(message, "🔄 **Обхожу ссылку, подожди пару секунд...**", parse_mode="Markdown")

    api_endpoint = f"https://api.bypass.vip/bypass?url={url}"

    try:
        response = requests.get(api_endpoint, timeout=15).json()

        if response.get("status") == "success":
            result = response.get("result")
            bot.edit_message_text(
                f"✅ **Готово! Твой результат/ключ:**\n\n`{result}`",
                chat_id=status_msg.chat.id,
                message_id=status_msg.message_id,
                parse_mode="Markdown"
            )
        else:
            bot.edit_message_text(
                "❌ Не удалось обойти эту ссылку.",
                chat_id=status_msg.chat.id,
                message_id=status_msg.message_id
            )
    except Exception:
        bot.edit_message_text(
            "⚠️ Ошибка сервера. Попробуй позже.",
            chat_id=status_msg.chat.id,
            message_id=status_msg.message_id
        )

if __name__ == "__main__":
    print("Бот SahurBypass успешно запущен!")
    bot.infinity_polling()
