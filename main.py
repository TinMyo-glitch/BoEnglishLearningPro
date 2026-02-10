import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Render Port Setup
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- သင်ခန်းစာ Content များ (Database အသေးစား) ---
LESSONS = {
    'level_basic': "💡 **Basic Level (အခြေခံ)**\n\nသင်ခန်းစာ (၁) - Greetings\nHello, Hi, How are you?\n\nသင်ခန်းစာ (၂) - Pronouns\nI, You, We, They, He, She, It...",
    'level_inter': "📘 **Intermediate Level (အလယ်အလတ်)**\n\nသင်ခန်းစာ (၁) - Tenses\nPresent Simple vs Present Continuous\n\nသင်ခန်းစာ (၂) - Modals\nCan, Could, Should, Must...",
    'level_adv': "🎓 **Advanced Level (အဆင့်မြင့်)**\n\nသင်ခန်းစာ (၁) - Academic Writing\nHow to write a formal essay...\n\nသင်ခန်းစာ (၂) - Idioms\n'Piece of cake' ဆိုတာ အလွန်လွယ်ကူတာကို ဆိုလိုတာပါ..."
}

# /start နှိပ်ရင် ခလုတ်တွေ ပြမယ့် Function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟢 Basic (အခြေခံ)", callback_data='level_basic')],
        [InlineKeyboardButton("🟡 Intermediate (အလယ်အလတ်)", callback_data='level_inter')],
        [InlineKeyboardButton("🔴 Advanced (အဆင့်မြင့်)", callback_data='level_adv')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "English Learning Bot မှ ကြိုဆိုပါတယ်။\nသင်ယူလိုတဲ့ Level ကို ရွေးချယ်ပါ -", 
        reply_markup=reply_markup
    )

# ခလုတ်နှိပ်လိုက်ရင် သင်ခန်းစာပြမယ့် Function
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Loading လည်နေတာကို ရပ်တန့်စေဖို့
    
    level_key = query.data
    content = LESSONS.get(level_key, "သင်ခန်းစာ ရှာမတွေ့ပါ။")
    
    # Back button လေးပါ ထပ်ထည့်ပေးမယ်
    back_keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    await query.edit_message_text(text=content, reply_markup=reply_markup, parse_mode='Markdown')

# Menu ပြန်သွားဖို့ Function
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🟢 Basic (အခြေခံ)", callback_data='level_basic')],
        [InlineKeyboardButton("🟡 Intermediate (အလယ်အလတ်)", callback_data='level_inter')],
        [InlineKeyboardButton("🔴 Advanced (အဆင့်မြင့်)", callback_data='level_adv')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("သင်ယူလိုတဲ့ Level ကို ထပ်မံရွေးချယ်ပါ -", reply_markup=reply_markup)

def main():
    Thread(target=run).start()
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern='back_to_menu'))
    application.add_handler(CallbackQueryHandler(handle_callback)) # level_ တွေအတွက်

    print("Bot is starting with menus...")
    application.run_polling()

if __name__ == '__main__':
    main()
