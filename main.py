import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- ၁။ Render Port အတွက် Flask Setup ---
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- ၂။ သင်ခန်းစာ Content များ (ဒီမှာ စာတွေ စိတ်ကြိုက်ပြင်နိုင်ပါတယ်) ---
LESSONS = {
    'level_basic': """
🟢 **Basic Level (အခြေခံ)**

**Lesson 1: Greetings (နှုတ်ဆက်ခြင်း)**
- Hello / Hi (မင်္ဂလာပါ)
- How are you? (နေကောင်းလား?)
- Nice to meet you. (တွေ့ရတာ ဝမ်းသာပါတယ်)

**Lesson 2: Pronouns (နာမ်စားများ)**
- I (ကျွန်တော်/ကျွန်မ)
- You (မင်း/ခင်ဗျား)
- We (ကျွန်တော်တို့)
""",
    'level_inter': """
🟡 **Intermediate Level (အလယ်အလတ်)**

**Lesson 1: Present Simple Tense**
- ပုံမှန်လုပ်လေ့ရှိတဲ့ အလေ့အကျင့်တွေကို ပြောတဲ့အခါ သုံးပါတယ်။
- Structure: Subject + Verb 1
- Example: I drink coffee every morning.

**Lesson 2: Giving Advice**
- "Should" ကို သုံးပြီး အကြံပေးနိုင်ပါတယ်။
- Example: You should take a rest.
""",
    'level_adv': """
🔴 **Advanced Level (အဆင့်မြင့်)**

**Lesson 1: Idioms (စကားပုံများ)**
- *Piece of cake:* အလွန်လွယ်ကူသောအရာ။
- *Break a leg:* ကံကောင်းပါစေ (Good luck)။

**Lesson 2: Formal Email Writing**
- Dear Hiring Manager,
- I am writing to express my interest in...
"""
}

# --- ၃။ Bot ရဲ့ အလုပ်လုပ်ပုံ (Functions) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ခလုတ်လှလှလေးများ တည်ဆောက်ခြင်း
    keyboard = [
        [InlineKeyboardButton("🟢 Basic (အခြေခံ)", callback_data='level_basic')],
        [InlineKeyboardButton("🟡 Intermediate (အလယ်အလတ်)", callback_data='level_inter')],
        [InlineKeyboardButton("🔴 Advanced (အဆင့်မြင့်)", callback_data='level_adv')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "English Learning Bot မှ ကြိုဆိုပါတယ်။ သင်ယူလိုတဲ့ Level ကို ရွေးချယ်ပါ -", 
        reply_markup=reply_markup
    )

async def handle_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # နှိပ်လိုက်တဲ့ ခလုတ်အလိုက် စာသားထုတ်ပေးခြင်း
    level_content = LESSONS.get(query.data, "သင်ခန်းစာ မရှိသေးပါ။")
    
    # Back button လေးပါ ထည့်ပေးမယ်
    back_btn = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
    
    await query.edit_message_text(
        text=level_content, 
        reply_markup=InlineKeyboardMarkup(back_btn),
        parse_mode='Markdown'
    )

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Menu ကို ပြန်ပြခြင်း
    keyboard = [
        [InlineKeyboardButton("🟢 Basic (အခြေခံ)", callback_data='level_basic')],
        [InlineKeyboardButton("🟡 Intermediate (အလယ်အလတ်)", callback_data='level_inter')],
        [InlineKeyboardButton("🔴 Advanced (အဆင့်မြင့်)", callback_data='level_adv')]
    ]
    await query.edit_message_text("သင်ယူလိုတဲ့ Level ကို ထပ်မံရွေးချယ်ပါ -", reply_markup=InlineKeyboardMarkup(keyboard))

# --- ၄။ Main Function (Bot ကို စတင်ခြင်း) ---
def main():
    Thread(target=run).start() # Flask ကို အနောက်မှာ run ထားမယ်
    
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern='back_to_menu'))
    application.add_handler(CallbackQueryHandler(handle_click))

    print("Bot is starting with Interactive Menus...")
    application.run_polling()

if __name__ == '__main__':
    main()
