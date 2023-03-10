from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def answer_button(user_id):
    markup = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text = "ðJavob berish",
                    callback_data=f"answer:{user_id}"
                )
            ]
        ]
    )
    return markup


yes_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = "ð Ha", callback_data="yes"),
            InlineKeyboardButton(text = "ð Yo'q", callback_data = "no")
        ]
    ]
)