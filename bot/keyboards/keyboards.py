from aiogram import types


def get_report_kb(user_id: int) -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="⚠ Пожаловаться", callback_data=f"report_{user_id}")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_ban_kb(user_id: int) -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="🚫 Забанить", callback_data=f"ban_{user_id}")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
