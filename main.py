import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram bot tokenini environment variable'dan olish
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Gemini API kalitini environment variable'dan olish
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def ask_gemini(user_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    data = {
        "contents": [{
            "parts": [{
                "text": f"Sening isming ORBIT AI 💎. O'zingni har doim ORBIT AI deb tanishtir. Savollarga qisqa va aniq javob ber. Savol: {user_text}"
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
        "Men **ORBIT AI**man (Gemini 3.5 Flash asosida) 💎\n"
        "Sizning shaxsiy sun'iy intellekt yordamchingizman. Savolingizni yozing."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    waiting = await update.message.reply_text("🤔 ORBIT AI o'ylayapti...")
    
    answer = await ask_gemini(user_text)
    await waiting.edit_text(answer)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 ORBIT AI (Gemini 3.5 Flash) ISHGA TUSHDI!")
    app.run_polling()

if __name__ == "__main__":
    main()
    
