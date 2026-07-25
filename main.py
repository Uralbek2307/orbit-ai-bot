import os
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TELEGRAM_BOT_TOKEN = "8888432167:AAGtMhKxnkwsYevWAhuVHghVOUUTZ2HyL6Q"
GEMINI_API_KEY = "AQ.Ab8RN6IX5NVGEC16q0Zeoah6RlGTHgJoKv1djECxKMM68Vp-vw"

async def ask_gemini(user_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{
                "text": f"Sening isming ORBIT AI 💎🤖. O'zingni har doim ORBIT AI deb tanishtir. Savolga o'zbek tilida qisqa va aniq javob ber: {user_text}"
            }]
        }]
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Xatosi: {response.json().get('error', {}).get('message', response.text)}"
    except Exception as e:
        return f"Ulanish xatosi: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Assalomu alaykum!\n\n"
        "Men **ORBIT AI**man (Gemini 3.5 Flash asosida) 💎🤖\n"
        "Sizning shaxsiy sun'iy intellekt yordamchingizman. Savolingizni yozing."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    waiting = await update.message.reply_text("🤔 ORBIT AI o'ylayapti...")
    answer = await ask_gemini(user_text)
    await waiting.edit_text(answer)

async def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 ORBIT AI (Gemini 3.5 Flash) 24/7 ISHGA TUSHDI!")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    
