from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard = [
        [
            KeyboardButton(
                text = "✍️ Savol yuborish"
            )
        ]
    ]
)