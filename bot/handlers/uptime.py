import time

from aiogram import F, types
from aiogram.filters import Command
from handlers.common import router
from main import start_time


@router.message(F.text, Command("uptime"))
async def uptime(message: types.Message) -> None:
    await message.answer(f"Uptime: {round(time.time() - start_time)} seconds")
