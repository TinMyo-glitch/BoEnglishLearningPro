import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- ၁။ Render Port Setup ---
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- ၂။ သင်ခန်းစာ Content များ (အပြည့်အစုံ) ---
LESSONS = {
    'level_basic': """
🟢 **Basic Level (အခြေခံ)**

**Lesson 1: Verb 'to be'**
- I am (ကျွန်တော် ဖြစ်သည်/ရှိသည်)
- You are (မင်း ဖြစ်သည်/ရှိသည်)
- He/She is (သူ/သူမ ဖြစ်သည်/ရှိသည်)
Ex: I am a student. (ကျွန်တော် ကျောင်းသားတစ်ယောက်ပါ။)

**Lesson 2: Simple Present Tense**
- နေ့စဉ်လုပ်နေကျ အလုပ်တွေကို ပြောရင် သုံးပါတယ်။
- I eat rice everyday. (ကျွန်တော် နေ့တိုင်း ထမင်းစားတယ်။)
""",
    'level_inter': """
🟡 **Intermediate Level (အလယ်အလတ်)**

**Lesson 1: Past Continuous Tense**
- အတိတ်မှာ လုပ်နေဆဲဖြစ်တဲ့ အကြောင်းအရာ။
- Structure: Was/Were + V-ing
- Ex: I was sleeping when you called. (မင်းဖုန်းဆက်တုန်းက ငါအိပ်နေတာ။)

**Lesson 2: Comparative**
- နှိုင်းယှဉ်ခြင်း (More/ -er)
- Ex: This car is faster than that one.
""",
    'level_adv': """
🔴 **Advanced Level (အဆင့်မြင့်)**

**Lesson 1: Present Perfect Continuous**
- အတိတ်ကစပြီး အခုထိ လုပ်နေတုန်းပဲ ရှိသေးတဲ့အရာ။
- Ex: I have been waiting for 3 hours. (ငါစောင့်နေတာ ၃ နာရီတောင် ရှိပြီ။)

**Lesson 2: Business Idioms**
- 'Call it a day' = အလုပ်ရပ်နားကြစို့။
- 'Get the ball rolling' = အလုပ်တစ်ခု စလုပ်ကြစို့။
"""
}

# --- ၃။ Quiz မေးခွန်းများ (Question Bank) ---
# Format: [မေးခွန်း, [အဖြေ ၁, အဖြေ ၂, ...], အဖြေမှန်နံပါတ် (0 ကစရေပါ)]
QUIZZES = {
    'quiz_basic': ["'I ___ a doctor.' ကွက်လပ်ဖြည့်ပါ။", ["is", "am", "are"], 1], # 1 ဆိုတာ 'am'
    'quiz_inter': ["'She was ____ TV.' ဘယ်ဟာမှန်သလဲ?", ["watch", "watched", "watching"], 2], # 2 ဆိုတာ 'watching'
    'quiz_adv': ["'Call it a day' ရဲ့ အဓိပ္ပာယ်က?", ["Stop working", "Start working", "Holiday"], 0] # 0 ဆိုတာ 'Stop working'
}

# --- ၄။ Bot Functions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟢 Basic Level", callback_data='level_basic')],
        [InlineKeyboardButton("🟡 Intermediate Level", callback_data='level_inter')],
        [InlineKeyboardButton("🔴 Advanced Level", callback_data='level_adv')]
    ]
    await update.message.reply_text(
        "📚 **English Learning Bot** မှ ကြိုဆိုပါတယ်။\nသင့် Level ကို ရွေးချယ်ပါ -", 
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # သင်ခန်းစာ ပြမယ့်အပိုင်း
    if data.startswith('level_'):
        content = LESSONS.get(data)
        
        # Quiz ဖြေမလား ခလုတ်လေး ထပ်ထည့်မယ်
        quiz_key = data.replace('level', 'quiz') # e.g., level_basic -> quiz_basic
        keyboard = [
            [InlineKeyboardButton("✍️ Take Quiz (လေ့ကျင့်ခန်းလုပ်မယ်)", callback_data=quiz_key)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]
        ]
        
        await query.edit_message_text(text=content, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    # Quiz မေးမယ့်အပိုင်း
    elif data.startswith('quiz_'):
        q_data = QUIZZES.get(data)
        question = q_data[0]
        options = q_data[1]
        correct_id = q_data[2]
        
        # Telegram Native Quiz ပို့မယ်
        await context.bot.send_poll(
            chat_id=update.effective_chat.id,
            question=question,
            options=options,
            type=Poll.QUIZ, # ဒါက အဖြေမှန်ရင် အမှန်ခြစ်ပြပေးမယ့် Mode
            correct_option_id=correct_id,
            explanation="အဖြေမှန်ကို ရွေးချယ်နိုင်ပါစေ!" 
        )

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context) # Start function ကို ပြန်ခေါ်လိုက်မယ်

def main():
    Thread(target=run).start()
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern='back_to_menu'))
    application.add_handler(CallbackQueryHandler(handle_menu_click)) 

    print("Bot is running with Quizzes...")
    application.run_polling()

if __name__ == '__main__':
    main()
