import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# 50 clean random words
words = [
    "sun", "moon", "star", "sky", "cloud",
    "river", "ocean", "tree", "leaf", "wind",
    "fire", "stone", "light", "shadow", "dream",
    "night", "day", "rain", "storm", "wave",
    "hill", "forest", "field", "dust", "sand",
    "ice", "snow", "thunder", "flash", "spark",
    "ember", "glow", "flare", "echo", "sound",
    "voice", "song", "tune", "melody", "rhythm",
    "path", "road", "trail", "track", "bridge",
    "gate", "door", "window", "wall", "tower"
]

# random word generator
def random_text():
    word = random.choice(words)
    number = random.randint(10, 999)
    return f"{word}{number}"

# generate unique aliases
def generate_aliases(email, count=10):
    username, domain = email.split("@")
    aliases = set()

    while len(aliases) < count:
        alias = f"{username}+{random_text()}@{domain}"
        aliases.add(alias)

    return list(aliases)

# send aliases
async def send_aliases(message, email):
    aliases = generate_aliases(email)

    text = "✅ Your 10 aliases:\n\n"
    text += "\n".join(f"`{a}`" for a in aliases)

    keyboard = [
        [InlineKeyboardButton("🔄 Generate Again", callback_data=email)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# handle message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()

    if not email.endswith("@gmail.com"):
        await update.message.reply_text("❌ Only Gmail addresses are allowed!")
        return

    await send_aliases(update.message, email)

# button handler
async def regenerate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    email = query.data
    await send_aliases(query.message, email)

# run bot
app = ApplicationBuilder().token("8758808437:AAFRbY8JpmQosbZ9qe8ys2IVoqR533WdTXE").build()

app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(CallbackQueryHandler(regenerate))

app.run_polling()