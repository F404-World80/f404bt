import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    keyboard = [
        [InlineKeyboardButton("🎨 HTML CSS Sharing", callback_data='html_css')],
        [InlineKeyboardButton("📡 StarlinkwifiHack", callback_data='starlink')],
        [InlineKeyboardButton("🔥 #F404", callback_data='f404')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"မဂ်လာပါ {user_name}\nF404-helperကို အသုံးပြုလို့ကျေးဇူးပါ\nအောက်ပါတို့မှ ရွေးချယ်ပေးပါ 👇",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    if choice == 'html_css':
        keyboard = [[InlineKeyboardButton("📥 Group ထဲဝင်ရန်", url="https://t.me/learnhtmlcs2")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🎨 **HTML CSS Sharing**\n\nHtml နှင့် CSS basic တွေကို အတူတူလေ့လာကြမဲ့ GP ကို join ပေးရန် 👇",
            reply_markup=reply_markup
        )
    elif choice == 'starlink':
        keyboard = [[InlineKeyboardButton("📥 Channel ထဲဝင်ရန်", url="https://t.me/smmoffical_55555")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="📡 **StarlinkwifiHack**\n\nStarlink နှင့်ပတ်သက်သော voucher code hack, ကျော်ခွသုံးဘာညာအတွက် join ရန် 👇",
            reply_markup=reply_markup
        )
    elif choice == 'f404':
        keyboard = [[InlineKeyboardButton("📥 Channel ထဲဝင်ရန်", url="https://t.me/learnbg404")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🔥 **#F404**\n\nHTML, CSS, Termux basic များနှင့် စွယ်စုံနည်းပညာဗဟုသုတ အစရှိသည်များ လေ့လာရန် join ပါ 👇",
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text(text="မှားယွင်းသွားပါပြီ။ နောက်တစ်ခါ ပြန်ရွေးပါ။")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ကျေးဇူးပါဗျ ❤️")

def main():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN not found!")
        return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
