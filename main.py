import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ English သင်ခန်းစာများ လေ့လာနိုင်ဖို့ ပြင်ဆင်နေပါပြီ။")

def main():
    # Render ပေါ်တင်ရင် Token ကို Environment Variable ကနေ ဖတ်တာ ပိုကောင်းပါတယ်
    token = os.getenv("BOT_TOKEN", "8461107529:AAEhXCsrUSNr4cC6AaiERvKYL21eTV6P_Ns")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
