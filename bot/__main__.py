import os
import logging
import asyncio
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv, find_dotenv

from bot.handlers import register_client_handlers


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    load_dotenv(find_dotenv())

    dp = Dispatcher()
    bot = Bot(token=os.getenv('token'))

    register_client_handlers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
