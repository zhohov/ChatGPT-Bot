from aiogram import types
from database import sqlite_users_db
from bot import *

admin = int(os.environ['admin_id'])


# @dp.message_handler(commands = ['statistics'])
async def command_statistics(message: types.Message):
    if message.chat.id == admin:
        number_of_users = sqlite_users_db.check_number_users()
        number_of_subscription_users = sqlite_users_db.check_number_of_subscription_users()
        await message.answer(
            f'Статистика по пользователям\n\nКоличество пользователей: {number_of_users}\nКоличество подписчиков: {number_of_subscription_users}')

    else:
        await message.answer('У вас недостаточно прав')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_statistics, commands=['statistics'])