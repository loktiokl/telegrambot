from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

TOKEN = os.environ.get("BOT_TOKEN")

# Exemple de produits
products = [
    {
        "id": "prod_1",
        "name": "Netflix 1 mois",
        "price": "2.99€",
        "description": "Compte partagé 1 écran, garanti 30j."
    },
    {
        "id": "prod_2",
        "name": "NordVPN 6 mois",
        "price": "5.99€",
        "description": "Connexion privée, multi-plateforme."
    }
]

# Commande /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Bienvenue sur notre boutique Telegram !\n\n"
        "🛍 Tape /products pour voir les articles\n"
        "📞 Tape /support pour contacter l’assistance\n"
        "🔒 Tape /privacy pour notre politique de confidentialité"
    )

# Commande /products
def products_command(update: Update, context: CallbackContext):
    for p in products:
        keyboard = [[
            InlineKeyboardButton("🛒 Acheter", callback_data=f"buy_{p['id']}")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"📦 {p['name']}\n💶 Prix : {p['price']}\nℹ️ {p['description']}",
            reply_markup=reply_markup
        )

# Quand l'utilisateur clique sur "Acheter"
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    data = query.data
    if data.startswith("buy_"):
        product_id = data.split("_")[1]
        product = next((p for p in products if p["id"].endswith(product_id)), None)
        if product:
            query.message.reply_text(
                f"✅ Tu as choisi *{product['name']}* à {product['price']}.\n"
                f"Pour commander, contacte @TonSupportTelegram ou utilise notre méthode de paiement automatique.",
                parse_mode="Markdown"
            )

# Commande /support
def support(update: Update, context: CallbackContext):
    update.message.reply_text("📞 Pour toute question, contacte-nous ici : @TonSupportTelegram")

# Commande /privacy
def privacy(update: Update, context: CallbackContext):
    update.message.reply_text("🔐 Toutes les commandes sont 100% anonymes. Aucune donnée n’est conservée.")

# Lancement du bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("products", products_command))
    dp.add_handler(CommandHandler("support", support))
    dp.add_handler(CommandHandler("privacy", privacy))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
