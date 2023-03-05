from aiogram import executor

from database import sqlite_users_db
from bot import dp

from handlers import client, admin

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)


async def on_startup(_):
    print('Bot working')
    sqlite_users_db.create_users_db()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
