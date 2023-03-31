from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


async def start_command(message: types.Message) -> Message:
    return await message.answer('Start')


def register_client_handlers(router: Router) -> None:
    router.message.register(start_command, Command(commands=['start']))
