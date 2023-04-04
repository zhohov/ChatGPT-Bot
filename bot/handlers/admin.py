from aiogram import types, Router
from aiogram.filters import Command
from sqlalchemy.orm import sessionmaker

from bot.database import get_user_number, get_user_number_with_subscription

router = Router()


async def statistics_command(message: types.Message, session_maker: sessionmaker) -> None:
    users = await get_user_number(session_maker=session_maker)
    users_with_subscription = await get_user_number_with_subscription(session_maker=session_maker)
    await message.answer(
        f'Статистика по пользователям\n\nКоличество пользователей: {users}'
        f'\nКоличество подписчиков: {users_with_subscription}')


def register_admin_handlers(router: Router) -> None:
    router.message.register(statistics_command, Command(commands=['statistics']), flags={'admin_check': 'admin_check'})
