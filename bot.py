from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv("7726733596:AAGZf8oPUoYuCpz712W8DgQIgnlSEWER6ZM")
WEBHOOK_DOMAIN = os.getenv("https://telegram-bot-mi46.onrender.com")

WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

ADMIN_CHAT_IDS = [648120374, 8191795574]
user_ids = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_ids[user.id] = user.username
    await update.message.reply_markdown(
        f"Здравствуй, {user.first_name}! Это бот канала *Хижина Шамана*\n\n"
        "Здесь вы можете задать любой интересующий вас вопрос. "
        "Я отвечу на него здесь или разберу подробно в рубрике \"Ответы на вопросы\" 🌱"
    )

# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    user_ids[user.id] = user.username

    for admin_id in ADMIN_CHAT_IDS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=(
                f"💬 Вопрос от {user.full_name} (@{user.username or 'без username'})\n"
                f"ID: `{user.id}`\n\n{message}"
            ),
            parse_mode='Markdown'
        )

    await update.message.reply_text(
        "Благодарю за обращение! Постараюсь ответить в ближайшее время.\n\nС любовью,\nЯра ♥️"
    )

# Команда /reply для админов
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_CHAT_IDS:
        await update.message.reply_text("⛔️ У вас нет доступа к этой команде.")
        return

    try:
        user_id = int(context.args[0])
        reply_text = ' '.join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=reply_text)
        await update.message.reply_text("✅ Ответ отправлен.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

# Запуск бота (WEBHOOK)
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен по webhook...")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=WEBHOOK_URL
    )