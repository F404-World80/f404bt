import os
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ========== Configuration ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 7825705562
USER_DATA_FILE = "users.txt"

# ========== Flask Web Server ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ========== Logging ==========
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ========== User Functions ==========
def save_user(user_id, username, first_name):
    try:
        with open(USER_DATA_FILE, "r") as f:
            users = f.readlines()
    except FileNotFoundError:
        users = []
    
    for line in users:
        if str(user_id) in line:
            return
    
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{user_id}|{username or 'No username'}|{first_name}\n")
    print(f"✅ User saved: {user_id} - {username} - {first_name}")

def get_main_keyboard():
    keyboard = [
        [KeyboardButton("🎨 HTML CSS Sharing")],
        [KeyboardButton("📡 StarlinkwifiHack")],
        [KeyboardButton("🔥 #F404")],
        [KeyboardButton("📊 Report")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ========== Inline Keyboards ==========
def get_starlink_menu():
    """Starlink Main Menu"""
    keyboard = [
        [InlineKeyboardButton("📥 Channel ထဲဝင်ရန်", url="https://t.me/smmoffical_55555")],
        [InlineKeyboardButton("💰 အရောင်းနှင့် ဈေးနှုန်းများ", callback_data='starlink_prices')],
        [InlineKeyboardButton("🤖 Voucher Code Hack Bot", callback_data='voucher_bot')],
        [InlineKeyboardButton("📖 Bot ရှိနားလည်သူ Src Script", callback_data='src_script')],
        [InlineKeyboardButton("⏰ နာရီပိုင်းအသုံးပြုရန် Voucher", callback_data='hourly_voucher')],
        [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_prices_menu():
    """ဈေးနှုန်း Sub-menu"""
    keyboard = [
        [InlineKeyboardButton("💵 Bypass Price", callback_data='bypass_price')],
        [InlineKeyboardButton("🏷️ Voucher Code Hack Price", callback_data='voucher_price')],
        [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_starlink')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_starlink():
    keyboard = [
        [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_starlink')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== Bot Handlers ==========
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
        reply_markup = get_starlink_menu()
        await update.message.reply_text(
            text="📡 **StarlinkwifiHack**\n\nအောက်ပါတို့မှ ရွေးချယ်ပေးပါ 👇",
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
        except FileNotFoundError:
            await update.message.reply_text("User မရှိသေးပါဘူး။")
            return
        
        total = len(users)
        active = 0
        blocked = 0
        report = f"📊 **User Report**\n\nစုစုပေါင်း: {total} ဦး\n\n"
        
        for line in users:
            try:
                parts = line.strip().split("|")
                if len(parts) >= 3:
                    user_id_line = parts[0]
                    username = parts[1]
                    first_name = parts[2]
                    
                    try:
                        await context.bot.send_chat_action(chat_id=int(user_id_line), action="typing")
                        active += 1
                        status = "✅ Active"
                    except Exception:
                        blocked += 1
                        status = "❌ Blocked"
                    
                    report += f"• {first_name} (@{username}) - {status}\n"
            except Exception:
                pass
        
        report += f"\n✅ Active: {active}\n❌ Blocked: {blocked}"
        
        if len(report) > 4000:
            for i in range(0, len(report), 4000):
                await update.message.reply_text(report[i:i+4000])
        else:
            await update.message.reply_text(report)
    
    else:
        await update.message.reply_text("ကျေးဇူးပါဗျ ❤️")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    
    # ===== Back Buttons =====
    if choice == 'back_to_main':
        keyboard = get_main_keyboard()
        await query.edit_message_text(
            text="အောက်ပါတို့မှ ရွေးချယ်ပေးပါ 👇",
            reply_markup=keyboard
        )
    
    elif choice == 'back_to_starlink':
        reply_markup = get_starlink_menu()
        await query.edit_message_text(
            text="📡 **StarlinkwifiHack**\n\nအောက်ပါတို့မှ ရွေးချယ်ပေးပါ 👇",
            reply_markup=reply_markup
        )
    
    # ===== Starlink Main Menu =====
    elif choice == 'starlink_prices':
        reply_markup = get_prices_menu()
        await query.edit_message_text(
            text="💰 **အရောင်းနှင့် ဈေးနှုန်းများ**\n\nအောက်ပါတို့မှ ရွေးချယ်ပေးပါ 👇",
            reply_markup=reply_markup
        )
    
    elif choice == 'voucher_bot':
        keyboard = [
            [InlineKeyboardButton("📖 အသေးစိတ်ရှင်းလင်းချက်ကြည့်ရန်", callback_data='voucher_bot_detail')],
            [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_starlink')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🤖 **Voucher Code Hack Bot**\n\n"
                 "Bot ဝယ်ပြီး ကိုယ်တိုင် code တွေ စိတ်ကြိုက်ရှာမယ်ဆိုရင်\n\n"
                 "💰 1 month = 35,000 Ks",
            reply_markup=reply_markup
        )
    
    elif choice == 'src_script':
        keyboard = [
            [InlineKeyboardButton("📖 အသေးစိတ်ရှင်းလင်းချက်ကြည့်ရန်", callback_data='src_script_detail')],
            [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_starlink')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="📖 **Bot ရှိနားလည်သူ Src Script**\n\n"
                 "Bot ရှိပြီး နားလည်သူများ\n"
                 "Open Source Script ဝယ်ယူလိုလျှင်\n\n"
                 "💰 40,000 Ks",
            reply_markup=reply_markup
        )
    
    elif choice == 'hourly_voucher':
        keyboard = [
            [InlineKeyboardButton("📖 အသေးစိတ်ရှင်းလင်းချက်ကြည့်ရန်", callback_data='hourly_voucher_detail')],
            [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_starlink')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="⏰ **နာရီပိုင်းအသုံးပြုရန် Voucher Code**\n\n"
                 "1 နာရီ code\n"
                 "2 နာရီ code\n"
                 "...အစရှိသဖြင့် ရှိပါသေးတယ်\n\n"
                 "ကျနော့်စီကဝယ်တဲ့ code နဲ့လည်း\n"
                 "Ruijie WiFi old/new မှာ ထည့်သွင်းပြီး\n"
                 "အသုံးပြုလို့ရမှာပါ",
            reply_markup=reply_markup
        )
    
    # ===== Prices Sub-menu =====
    elif choice == 'bypass_price':
        keyboard = [
            [InlineKeyboardButton("📖 အသေးစိတ်ရှင်းလင်းချက်ကြည့်ရန်", callback_data='bypass_detail')],
            [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_starlink')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="💵 **Bypass Price**\n\n"
                 "📅 7 days = 5,000 Ks\n"
                 "📅 30 days = 15,000 Ks\n"
                 "📅 90 days = 30,000 Ks (Normal Price)\n\n"
                 "🔥 **Promo Price** (လျော့ဈေး)\n"
                 "ပထမဆုံးဝယ်ယူသူ 5 ဦးအတွက် အထူးဈေးနှုန်း!",
            reply_markup=reply_markup
        )
    
    elif choice == 'voucher_price':
        keyboard = [
            [InlineKeyboardButton("📖 အသေးစိတ်ရှင်းလင်းချက်ကြည့်ရန်", callback_data='voucher_detail')],
            [InlineKeyboardButton("🔙 နောက်သို့", callback_data='back_to_starlink')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🏷️ **Voucher Code Hack Price**\n\n"
                 "🔢 ဂဏန်း 6 လုံး only\n"
                 "(ဥပမာ: 185364)\n\n"
                 "📦 Code 100 ဝယ်ရင် = 15,000 Ks",
            reply_markup=reply_markup
        )
    
    # ===== Detail Buttons =====
    elif choice == 'bypass_detail':
        keyboard = get_back_to_starlink()
        await query.edit_message_text(
            text="📖 **Bypass အသေးစိတ်**\n\n"
                 "ရိုးရိုး normal ကျနော်တို့ အရင်လို\n"
                 "Bypass လုပ်ပြီး အသုံးပြုသလိုပါပဲ\n"
                 "အရမ်းကွာခြားတာ သိပ်မရှိပါဘူး",
            reply_markup=keyboard
        )
    
    elif choice == 'voucher_detail':
        keyboard = get_back_to_starlink()
        await query.edit_message_text(
            text="📖 **Voucher Code အသေးစိတ်**\n\n"
                 "(code နဲ့ပက်သက်ပီး အသေးစိတ်လဲ DM မှာလာမေးပေးပါ)",
            reply_markup=keyboard
        )
    
    elif choice == 'voucher_bot_detail':
        keyboard = get_back_to_starlink()
        await query.edit_message_text(
            text="📖 **Voucher Code Hack Bot အသေးစိတ်**\n\n"
                 "(Bot တစ်ခုလုံး ဝယ်လိုက်ပီး code တေကို မိမိစိတ်ကြိုက်ရှာလို့မှာပါ)",
            reply_markup=keyboard
        )
    
    elif choice == 'src_script_detail':
        keyboard = get_back_to_starlink()
        await query.edit_message_text(
            text="📖 **Src Script အသေးစိတ်**\n\n"
                 "(Script file ဝယ်ယူလိုသူများအတွက်ပါ)",
            reply_markup=keyboard
        )
    
    elif choice == 'hourly_voucher_detail':
        keyboard = get_back_to_starlink()
        await query.edit_message_text(
            text="📖 **နာရီပိုင်း Voucher အသေးစိတ်**\n\n"
                 "(နာရီပိုင်းနဲ့ပက်သက်ပီး\nဈေးနှုန်းအတက်ကျရှိပါတယ် အသေးစိတ်တော့ \n@errorstar_55555မှာ လာမေးပေးပါ)",
            reply_markup=keyboard
        )

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("你不是 OWNER")
        return
    
    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("ပုံစံ: /broadcast စာသား")
        return
    
    try:
        with open(USER_DATA_FILE, "r") as f:
            users = f.readlines()
    except FileNotFoundError:
        await update.message.reply_text("User မရှိသေးပါဘူး။")
        return
    
    sent = 0
    failed = 0
    for line in users:
        try:
            parts = line.strip().split("|")
            if len(parts) >= 1:
                user_id = int(parts[0])
                await context.bot.send_message(chat_id=user_id, text=message)
                sent += 1
        except Exception:
            failed += 1
    
    await update.message.reply_text(
        f"✅ စာပို့ပြီးပါပြီ။\n\n"
        f"✅ အောင်မြင်: {sent} ဦး\n"
        f"❌ မအောင်မြင်: {failed} ဦး"
    )

# ========== Main ==========
def main():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN not found!")
        return
    
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    print("🌐 Web Server started on port 8080")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    
    print("🤖 Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()