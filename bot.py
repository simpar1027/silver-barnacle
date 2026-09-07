import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в Railway")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("📸 Код изображения")
    keyboard.add("✂️ Убрать фон")
    keyboard.add("🔗 Получить ссылку")
    keyboard.add("💻 Формат кода")
    keyboard.add("❓ Помощь")

    bot.send_message(
        message.chat.id,
        """👋 Привет!

Здесь ты можешь узнать код от фото и вставить его в свой код!

📸 Присылай своё фото → если надо, уберём фон → 🖼️ скинем результат вместе со ссылкой.

Выбери действие ниже:""",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.text == "📸 Код изображения":
        bot.reply_to(message, "📸 Отправь мне изображение.")

    elif message.text == "✂️ Убрать фон":
        bot.reply_to(
            message,
            "✂️ Отправь изображение, у которого нужно убрать фон."
        )

    elif message.text == "🔗 Получить ссылку":
        bot.reply_to(
            message,
            "🔗 Отправь изображение, и я подготовлю ссылку."
        )

    elif message.text == "💻 Формат кода":
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(
            types.InlineKeyboardButton("HTML", callback_data="html"),
            types.InlineKeyboardButton("CSS", callback_data="css")
        )

        keyboard.add(
            types.InlineKeyboardButton(
                "Markdown",
                callback_data="markdown"
            )
        )

        bot.send_message(
            message.chat.id,
            "💻 Выбери формат:",
            reply_markup=keyboard
        )

    elif message.text == "❓ Помощь":
        bot.reply_to(
            message,
            """❓ Помощь

📸 Код изображения — получить готовый код.
✂️ Убрать фон — обработать изображение.
🔗 Получить ссылку — получить ссылку.
💻 Формат кода — выбрать HTML, CSS или Markdown."""
        )


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    formats = {
        "html": "HTML",
        "css": "CSS",
        "markdown": "Markdown"
    }

    if call.data in formats:
        bot.answer_callback_query(call.id)

        bot.send_message(
            call.message.chat.id,
            f"✅ Выбран формат: {formats[call.data]}"
        )


print("порнуха запущена!")

bot.infinity_polling()
