import os
import logging
import asyncio
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import URL

from bot.database import create_async_engine, get_session_maker
from bot.handlers import register_client_handlers
from middlewares.registration_check import RegistrationCheck
from middlewares.checking_availability_of_the_request import RequestsCheck


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    load_dotenv(find_dotenv())

    dp = Dispatcher()
    bot = Bot(token=os.getenv('token'))
    dp.message.middleware(RegistrationCheck())
    dp.message.middleware(RequestsCheck())

    register_client_handlers(dp)

    postgres_url = URL.create(
         drivername='postgresql+asyncpg',
         username=os.getenv('db_user'),
         password=os.getenv('db_user_password'),
         host='localhost',
         database=os.getenv('db_name'),
         port=os.getenv('db_port')
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
