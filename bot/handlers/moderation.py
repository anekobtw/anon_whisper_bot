from aiogram import F, types
from aiogram.filters import Command

from database import MessagesManager, UsersManager
from handlers.common import router
from keyboards import get_ban_kb

admins = [1718021890]


@router.message(F.text, Command("ban"))
async def ban_with_command(message: types.Message):
    if message.from_user.id in admins:
        user_id = message.text.split(" ")[1]
        UsersManager().ban_user(user_id)
        await message.answer(f"Пользователь {user_id} забанен!")
    else:
        await message.answer("У тебя нет доступа к этой команде")


@router.message(F.text, Command("unban"))
async def unban_with_command(message: types.Message):
    if message.from_user.id in admins:
        user_id = message.text.split(" ")[1]
        UsersManager().unban_user(user_id)
        await message.answer(f"Пользователь {user_id} разбанен!")
    else:
        await message.answer("У тебя нет доступа к этой команде")


@router.callback_query(F.data.startswith("report_"))
async def report(callback: types.CallbackQuery):
    if MessagesManager().is_in_db(callback.message.message_id):
        return
    MessagesManager().insert_message(callback.message.message_id)
    user_id = callback.data.split("_")[1]
    await callback.bot.send_message(
        chat_id=1718021890,
        text=f"<b>Поступил репорт!\nАйди пользователя: {user_id}</b>\n\n{callback.message.text}",
        reply_markup=get_ban_kb(user_id),
    )


@router.callback_query(F.data.startswith("ban_"))
async def ban_with_button(callback: types.CallbackQuery):
    if callback.from_user.id in admins:
        user_id = callback.data.split("_")[1]
        UsersManager().ban_user(user_id)
        await callback.message.answer(f"Пользователь {user_id} забанен!")
    else:
        await callback.answer("У тебя нет доступа к этой команде")
