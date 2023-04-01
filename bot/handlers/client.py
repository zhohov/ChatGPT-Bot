from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


async def start_command(message: types.Message) -> Message:
    return await message.answer('Start')


async def request_command(message: types.Message) -> None:
    await message.answer('Request!')


def register_client_handlers(router: Router) -> None:
    router.message.register(start_command, Command(commands=['start']), flags={'registration_check': 'registration_check'})
    router.message.register(request_command, Command(commands=['request']), flags={'update_requests': 'update_requests'})
