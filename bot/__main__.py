import os
import logging
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import URL

from bot.database import create_async_engine, get_session_maker
from bot.handlers import register_start_handlers, register_profile_handlers, register_admin_handlers, \
    register_response_handlers, register_feedback_handlers, register_buy_handlers, bot_commands
from bot.middlewares.registration_check import RegistrationCheck
from bot.middlewares.checking_availability_of_the_request import RequestsCheck
from bot.middlewares.admin_check import AdminCheck


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    load_dotenv(find_dotenv())

    commands = []
    for cmd in bot_commands:
        commands.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher()
    bot = Bot(token=os.getenv('token'))
    await bot.set_my_commands(commands=commands)

    dp.message.middleware(RegistrationCheck())
    dp.message.middleware(RequestsCheck())
    dp.message.middleware(AdminCheck())

    register_start_handlers(dp)
    register_profile_handlers(dp)
    register_buy_handlers(dp)
    register_feedback_handlers(dp)
    register_admin_handlers(dp)
    register_response_handlers(dp)

    postgres_url = URL.create(
         drivername='postgresql+asyncpg',
         username=os.getenv('POSTGRES_USER'),
         password=os.getenv('POSTGRES_PASSWORD'),
         host=os.getenv('POSTGRES_HOST'),
         database=os.getenv('POSTGRES_DB'),
         port=os.getenv('POSTGRES_PORT')
     )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
