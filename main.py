import os
import asyncio
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Render port talab qilgani uchun kichik Flask veb-server
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "ORBIT AI Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

TELEGRAM_BOT_TOKEN = "8888432167:AAHTaoQIDAkYvkS9cCTcQwAOVDUgHmNx3ZI"
OPENAI_API_KEY = "Sk-svcacct-hmSgAEUl4pZsft5HhS6Yh6JYsOWq98IVhHLeVf9gX-lt25V4IXBMCuNCrt0LF-8iisiZ-rfc8ET3BlbkFJ7sq1oZD53EZV7WErEh8Vc7i9YmCO9pimTJ5BkZUJDDFBH3-8y0bIfa0GRVcqY1-cT7gSQvPc8A"

async def ask_openai(user_text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Sening isming ORBIT AI 💎🤖. O'zingni har doim ORBIT AI deb tanishtir. Savolga o'zbek tilida qisqa va aniq javob ber."},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Xatosi: {response.json().get('error', {}).get('message', response.text)}"
    except Exception as e:
        return f"Ulanish xatosi: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Assalomu alaykum!\n\n"
        "Men **ORBIT AI**man (OpenAI asosida) 💎🤖\n"
        "Sizning shaxsiy sun'iy intellekt yordamchingizman. Savolingizni yozing."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    waiting = await update.message.reply_text("🤔 ORBIT AI o'ylayapti...")
    answer = await ask_openai(user_text)
    await waiting.edit_text(answer)

async def main():
    # Flask serverni alohida potokda ishga tushirish (Render port xatosini yo'qotadi)
    threading.Thread(target=run_flask, daemon=True).start()

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 ORBIT AI (OpenAI) 24/7 ISHGA TUSHDI!")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    stop_event = asyncio.Event()
    await stop_event.wait()

if __name__ == "__main__":
    asyncio.run(main())
    
