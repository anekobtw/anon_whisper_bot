import os

from aiogram import F, Router, types
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import deep_linking
from dotenv import load_dotenv

from database import UsersManager
from keyboards import get_report_kb

router = Router()


class SendForm(StatesGroup):
    message = State()


@router.message(F.text, Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text="Операция отменена.", reply_markup=types.ReplyKeyboardRemove())


@router.message(CommandStart(deep_link=True))
async def cmd_start_help(message: types.Message, command: CommandObject, state: FSMContext):
    UsersManager().create_user(message.from_user.id)

    if UsersManager().is_banned(message.from_user.id):
        await message.answer("К сожалению, ты был забанен.")
    else:
        user_id = int(command.args)
        await state.update_data(receiver_id=user_id)
        await state.set_state(SendForm.message)
        await message.answer("Отправь мне текст, который хочешь отправить пользователю.\n/cancel для отмены")


@router.message(CommandStart(deep_link=False))
async def start(message: types.Message):
    UsersManager().create_user(message.from_user.id)

    load_dotenv()
    deeplink = deep_linking.create_deep_link(os.getenv("BOT_TG_NICKNAME"), "start", payload=message.from_user.id)
    await message.answer(
        f"Привет, {message.from_user.full_name}! Это бот для отправки анонимных сообщений.\n\nОтправь свою ссылку друзьям и получи сообщения от них анонимные сообщения:\n{deeplink}"
    )


@router.message(F.text, Command("link"))
async def link(message: types.Message):
    load_dotenv()
    deeplink = deep_linking.create_deep_link(os.getenv("BOT_TG_NICKNAME"), "start", payload=message.from_user.id)
    await message.answer(f"Твоя личная ссылка, отправляй её друзьям:\n{deeplink}")


@router.message(F.text, Command("stats"))
async def stats(message: types.Message):
    user = UsersManager().get_user(message.from_user.id)
    ban_status = "Забанен" if user[3] == 1 else "Не забанен"
    await message.answer(f"<b>{message.from_user.full_name}</b>\n\nОтправлено сообщений: {user[1]}\nПолучено сообщений: {user[2]}\nСтатус бана: {ban_status}")


@router.message(SendForm.message)
async def process_message(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer("Произошла ошибка. Помни, что отправлять можно только текст и эмодзи.")
        await cancel_handler(message, state)
    else:
        user_data = await state.get_data()
        await message.bot.send_message(
            user_data["receiver_id"], text=f"<b>У тебя новое сообщение!</b>\n\n{message.text}", reply_markup=get_report_kb(message.from_user.id)
        )
        UsersManager().user_sent_message(message.from_user.id)
        UsersManager().user_received_message(user_data["receiver_id"])
        await state.clear()
        await message.answer("Отправлено!")
