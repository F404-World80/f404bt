import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 7825705562
USER_DATA_FILE = "users.txt"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def save_user(user_id, username, first_name):
    try:
        with open(USER_DATA_FILE, "r") as f:
            users = f.readlines()
    except:
        users = []
    
    for line in users:
        if str(user_id) in line:
            return
    
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{user_id}|{username or 'No username'}|{first_name}\n")

def get_main_keyboard():
    keyboard = [
        [KeyboardButton("🎨 HTML CSS Sharing")],
        [KeyboardButton("📡 StarlinkwifiHack")],
        [KeyboardButton("🔥 #F404")],
        [KeyboardButton("📊 Report")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username, user.first_name)
    
    user_name = update.effective_user.first_name
    reply_keyboard = get_main_keyboard()
    
    await update.message.reply_text(
        f"မဂ်လာပါ {user_name}\n#f404_helper ကို အသုံးပြုလို့ကျေးဇူးပါ\nအောက်ပါတို့မှ ရွေးချယ်ပေးပါ 👇",
        reply_markup=reply_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    if text == "🎨 HTML CSS Sharing":
        keyboard = [
            [InlineKeyboardButton("📥 Group ထဲဝင်ရန်", url="https://t.me/learnhtmlcs2")],
            [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text="🎨 **HTML CSS Sharing**\n\nHtml နှင့် CSS basic တွေကို အတူတူလေ့လာကြမဲ့ GP ကို join ပေးရန် 👇",
            reply_markup=reply_markup
        )
    
    elif text == "📡 StarlinkwifiHack":
        keyboard = [
            [InlineKeyboardButton("📥 Channel ထဲဝင်ရန်", url="https://t.me/smmoffical_55555")],
            [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text="📡 **StarlinkwifiHack**\n\nStarlink နှင့်ပတ်သက်သော voucher code hack, ကျော်ခွသုံးဘာညာအတွက် join ရန် 👇",
            reply_markup=reply_markup
        )
    
    elif text == "🔥 #F404":
        keyboard = [
            [InlineKeyboardButton("📥 Channel ထဲဝင်ရန်", url="https://t.me/learnbg404")],
            [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text="🔥 **#F404**\n\nHTML, CSS, Termux basic များနှင့် စွယ်စုံနည်းပညာဗဟုသုတ အစရှိသည်များ လေ့လာရန် join ပါ 👇",
            reply_markup=reply_markup
        )
    
    elif text == "📊 Report":
        if user_id != ADMIN_ID:
            await update.message.reply_text("ခင်ဗျား Admin မဟုတ်ပါဘူး။")
            return
        
        try:
            with open(USER_DATA_FILE, "r") as f:
                users = f.readlines()
        except:
            await update.message.reply_text("User မရှိသေးပါဘူး။")
            return
        
        total = len(users)
        active = 0
        blocked = 0
        report = f"📊 **User Report**\n\nစုစုပေါင်း: {total} ဦး\n\n"
        
        for line in users:
            try:
                user_id_line, username, first_name = line.strip().split("|")
                try:
                    await context.bot.send_chat_action(chat_id=user_id_line, action="typing")
                    active += 1
                    status = "✅ Active"
                except:
                    blocked += 1
                    status = "❌ Blocked"
                
                report += f"• {first_name} (@{username}) - {status}\n"
            except:
                pass
        
        report += f"\n✅ Active: {active}\n❌ Blocked: {blocked}"
        await update.message.reply_text(report)
    
    else:
        await update.message.reply_text("ကျေးဇူးပါဗျ ❤️")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    
    if choice == 'back_to_main':
        keyboard = get_main_keyboard()
        await query.edit_message_text(
            text="အောက်ပါတို့မှ ရွေးချယ်ပေးပါ 👇",
            reply_markup=keyboard
        )

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("ခင်ဗျား Admin မဟုတ်ပါဘူး။")
        return
    
    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("ပုံစံ: /broadcast စာသား")
        return
    
    try:
        with open(USER_DATA_FILE, "r") as f:
            users = f.readlines()
    except:
        await update.message.reply_text("User မရှိသေးပါဘူး။")
        return
    
    sent = 0
    for line in users:
        try:
            user_id = line.split("|")[0]
            await context.bot.send_message(chat_id=user_id, text=message)
            sent += 1
        except:
            pass
    
    await update.message.reply_text(f"စာပို့ပြီးပါပြီ။ {sent} ဦးဆီ ပို့ခဲ့တယ်။")

def main():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN not found!")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
