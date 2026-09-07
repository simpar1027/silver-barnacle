import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в Railway")

bot = telebot.TeleBot(TOKEN)

# Запоминаем выбранный формат для каждого пользователя
user_formats = {}


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


# Выбор формата кода
@bot.message_handler(func=lambda message: message.text == "💻 Формат кода")
def choose_format(message):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            "HTML",
            callback_data="format_html"
        ),
        types.InlineKeyboardButton(
            "CSS",
            callback_data="format_css"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "Markdown",
            callback_data="format_markdown"
        )
    )

    bot.send_message(
        message.chat.id,
        "💻 Выбери формат кода:",
        reply_markup=keyboard
    )


# Обработка выбора формата
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("format_")
)
def format_callback(call):
    format_name = call.data.replace("format_", "")

    user_formats[call.from_user.id] = format_name

    names = {
        "html": "HTML",
        "css": "CSS",
        "markdown": "Markdown"
    }

    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        f"✅ Формат выбран: {names[format_name]}\n\n"
        "Теперь отправь мне фотографию 📸"
    )


# Получение фотографии
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    try:
        # Получаем файл Telegram
        file_info = bot.get_file(message.photo[-1].file_id)

        # Ссылка на файл Telegram
        file_url = (
            f"https://api.telegram.org/file/bot"
            f"{TOKEN}/{file_info.file_path}"
        )

        # Узнаём выбранный формат
        selected_format = user_formats.get(
            message.from_user.id,
            "html"
        )

        # Создаём код
        if selected_format == "html":
            code = f'<img src="{file_url}" alt="Фото">'

        elif selected_format == "css":
            code = f'background-image: url("{file_url}");'

        else:
            code = f"![Фото]({file_url})"

        # Отправляем фото обратно
        bot.send_photo(
            message.chat.id,
            message.photo[-1].file_id,
            caption="🖼️ Фото получено!"
        )

        # Отправляем результат
        bot.send_message(
            message.chat.id,
            f"""🔗 Ссылка на изображение:

{file_url}

💻 Код ({selected_format.upper()}):

{code}"""
        )

    except Exception as error:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка при обработке изображения:\n\n{error}"
        )


# Кнопка "Код изображения"
@bot.message_handler(
    func=lambda message: message.text == "📸 Код изображения"
)
def image_code(message):
    bot.send_message(
        message.chat.id,
        "📸 Отправь мне фотографию.\n\n"
        "По умолчанию я подготовлю HTML-код."
    )


# Кнопка "Получить ссылку"
@bot.message_handler(
    func=lambda message: message.text == "🔗 Получить ссылку"
)
def get_link(message):
    bot.send_message(
        message.chat.id,
        "🔗 Отправь фотографию, и я дам ссылку на неё."
    )


# Кнопка "Убрать фон"
@bot.message_handler(
    func=lambda message: message.text == "✂️ Убрать фон"
)
def remove_background(message):
    bot.send_message(
        message.chat.id,
        "✂️ Функцию удаления фона добавим следующим этапом."
    )


# Помощь
@bot.message_handler(
    func=lambda message: message.text == "❓ Помощь"
)
def help_message(message):
    bot.send_message(
        message.chat.id,
        """❓ Помощь

📸 Код изображения — получить код изображения.

🔗 Получить ссылку — получить ссылку на изображение.

💻 Формат кода — выбрать HTML, CSS или Markdown.

✂️ Убрать фон — удалить фон изображения.

После выбора формата просто отправь фотографию 📸"""
    )


print("67! ГАЗАН! ЕГОР ГЕЙ!")

bot.infinity_polling()
