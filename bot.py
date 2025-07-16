
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import requests

TELEGRAM_TOKEN = "ВАШ_ТЕЛЕГРАМ_ТОКЕН"
OPENROUTER_API_KEY = "ВАШ_OPENROUTER_API_КЛЮЧ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я теперь умный бот с ИИ 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print("Пришло сообщение:", user_message)

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Отвечай дружелюбно и вежливо."},
                {"role": "user", "content": user_message}
            ]
        }
    )

    result = response.json()
    ai_reply = result["choices"][0]["message"]["content"]

    await update.message.reply_text(ai_reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("Бот с ИИ запущен. Ждёт сообщений...")
app.run_polling()
