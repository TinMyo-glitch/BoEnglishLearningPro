import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler

# Render အတွက် Port ဖွင့်ပေးမယ့် Flask app
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Render က ပေးတဲ့ Port ကို သုံးမယ်၊ မရှိရင် 8080 သုံးမယ်
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def main():
    # Web server ကို သီးသန့် Thread နဲ့ run မယ်
    Thread(target=run).start()

    # Bot logic
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Bot is online!")))
    
    application.run_polling()

if __name__ == '__main__':
    main()
