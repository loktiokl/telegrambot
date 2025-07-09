from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8150012447:AAG_6rkkda4rtMtkhV7FRWY9GrStI0ymEho"

catalogue = {
    "1": {"name": "Bitcoin", "price": "Crypto"},
    "2": {"name": "PayPal", "price": "PayPal"},
    "3": {"name": "Giftcard Amazon", "price": "Giftcard"},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{item['name']} - Paiement via {item['price']}", callback_data=f"pay_{item_id}")]
        for item_id, item in catalogue.items()
    ]
    await update.message.reply_text("Choisis un mode de paiement :", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("pay_"):
        item_id = data.split("_")[1]
        item = catalogue.get(item_id)
        if item:
            # Ici tu peux envoyer un lien de paiement ou instructions spécifiques selon le choix
            if item["price"] == "Crypto":
                await query.message.reply_text("Pour payer en crypto, envoie ton paiement à : 1BitcoinAdresseExemple12345")
            elif item["price"] == "PayPal":
                await query.message.reply_text("Payez via PayPal ici : https://paypal.me/toncompte")
            elif item["price"] == "Giftcard":
                await query.message.reply_text("Utilisez ce code Giftcard Amazon : AMAZON-GIFT-123456")
        else:
            await query.message.reply_text("Mauvais choix.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tape /start pour voir les options de paiement.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("help", help_command))
    app.run_polling()

if __name__ == "__main__":
    main()
