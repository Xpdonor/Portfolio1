from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import requests

API_KEY = 'bot token'
IDPAY_API_KEY = 'paiment site api'
CALLBACK_URL = 'https://yourdomain.com/verify'  

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    amount = 20000  # price

    data = {
        "order_id": str(chat_id),
        "amount": amount * 10,  # convert to rial
        "callback": CALLBACK_URL,
        "name": "buy config"
    }
    headers = {"X-API-KEY": IDPAY_API_KEY, "Content-Type": "application/json"}
    response = requests.post("https://api.idpay.ir/v1.1/payment", json=data, headers=headers).json()

    if "link" in response:
        button = InlineKeyboardButton("pay", url=response["link"])
        await update.message.reply_text("Click here for payment:", reply_markup=InlineKeyboardMarkup([[button]]))
    else:
        await update.message.reply_text("❌ Erorr.")

app = ApplicationBuilder().token(API_KEY).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
