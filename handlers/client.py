from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.message import ContentType
from datetime import datetime

from database import sqlite_users_db
from bot import *


# @dp.message_handler(commands = ['start'])
async def command_start(message: types.Message):
    sqlite_users_db.add_user(message.chat.id, message.chat.username)
    await message.answer(
        'Привет, наш Telegram-бот предоставляет доступ к ChatGPT - инновационной системе искусственного интеллекта, которая может использоваться для автоматической генерации текстовых ответов на вопросы. С ее помощью вы можете получать ответы на вопросы или создавать новый контент для своих проектов на основе искусственного интеллекта.\n\nДля использования нашего Telegram-бота вам нужно отправить боту запрос.')


# @dp.message_handler(commands = ['about'])
async def command_about(message: types.Message):
    await message.answer(
        'ChatGPT bot\n\nНаш Telegram-бот предоставляет доступ к ChatGPT - инновационной системе искусственного интеллекта, которая может использоваться для автоматической генерации текстовых ответов на вопросы. С ее помощью вы можете получать ответы на вопросы или создавать новый контент для своих проектов на основе искусственного интеллекта.\n\nДля использования нашего Telegram-бота вам нужно отправить боту запрос. В ответ на ваш запрос бот предоставит вам сгенерированный текстовый ответ на основе ChatGPT.\n\nChatGPT является очень мощным инструментом для генерации текстовых ответов на вопросы, и мы уверены, что наш Telegram-бот станет для вас незаменимым помощником в создании новых проектов на основе искусственного интеллекта. Не откладывайте использование нашего бота на завтра - начните прямо сейчас и получите доступ к самой передовой технологии искусственного интеллекта.')


# @dp.message_handler(commands = ['profile'])
async def command_profile(message: types.Message):
    if sqlite_users_db.check_subscription(message.chat.id):
        subscription_end_date = sqlite_users_db.check_subscription_end_date(message.chat.id) + 60 * 60 * 3
        end_date = datetime.fromtimestamp(subscription_end_date).strftime("%b %d %Y - %H:%M:%S")

        await message.answer(f'Профиль\n\nid: {message.chat.id}\nПодписка: есть\nОкончаниe подписки: {end_date}')

    else:
        user_responses = sqlite_users_db.check_responses(message.chat.id)
        user_max_responses = sqlite_users_db.check_max_responses(message.chat.id)

        await message.answer(
            f'Профиль\n\nid: {message.chat.id}\nПодписка: нет\nЗапросы:  {user_responses}/{user_max_responses}')


# @dp.message_handler(commands = ['buy'])
async def command_pay(message: types.Message):
    button = InlineKeyboardButton('Buy', callback_data='buy')
    keyboard = InlineKeyboardMarkup().add(button)
    await message.answer(
        'Подписка на 1 месяц\n\nПлатная подписка позволит вам отправлять неограниченное число запросов в течение 1 месяца\n\nЦена: 499.00р / месяц',
        reply_markup=keyboard)


# @dp.callback_query_handler(text = 'buy')
async def buy_month_subscribe(call: types.CallbackQuery):
    await bot.send_invoice(chat_id=call.from_user.id,
                           title='Подписка на месяц',
                           description='Платная подписка на ChatGPT бота даст вам возможность отправлять неограниченное число запросов в течение 1 месяца',
                           payload='month_sub',
                           provider_token=payments_token,
                           currency='RUB',
                           start_parameter='',
                           prices=[{'label': 'руб', 'amount': 49900}],
                           )


# @dp.pre_checkout_query_handler()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# @dp.message_handler(content_types = ContentType.SUCCESSFUL_PAYMENT)
async def successful_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'month_sub':
        await message.answer('Вы успешно приобрели подписку!')
        sqlite_users_db.update_subscription(message.chat.id)
        sqlite_users_db.update_subscription_end_date(message.chat.id)


# @dp.message_handler()
async def gpt_answer(message: types.Message):
    if sqlite_users_db.check_subscription(message.chat.id):
        date_now = datetime.today().replace(microsecond=0)
        timestamp_date_now = int(datetime.timestamp(date_now))
        subscription_end_date = sqlite_users_db.check_subscription_end_date(message.chat.id)
        delta = subscription_end_date - timestamp_date_now
        if delta > 0:
            await message.answer('Формируем ответ...')
            response = openai.Completion.create(model="text-davinci-003",
                                                prompt=message.text,
                                                temperature=0.9,
                                                max_tokens=700,
                                                top_p=1,
                                                frequency_penalty=0.0,
                                                presence_penalty=0.6,
                                                )
            await message.answer(response.choices[0].text)
            print(response)

        else:
            sqlite_users_db.remove_subscription(message.chat.id)
            sqlite_users_db.remove_subscription_end_date(message.chat.id)
            sqlite_users_db.remove_number_of_responses(message.chat.id)
            await message.answer('Ваша подписка закончилась')

    else:
        user_responses = sqlite_users_db.check_responses(message.chat.id)
        user_max_responses = sqlite_users_db.check_max_responses(message.chat.id)

        if user_responses < user_max_responses:
            user_responses += 1
            await message.answer(f'Количество запросов: {user_responses}/{user_max_responses}')
            sqlite_users_db.update_responses(message.chat.id, user_responses)
        else:
            await message.answer('Вы превысили количество запросов')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_about, commands=['help'])
    dp.register_message_handler(command_profile, commands=['profile'])
    dp.register_message_handler(command_pay, commands=['buy'])
    dp.register_callback_query_handler(buy_month_subscribe, text='buy')
    dp.register_pre_checkout_query_handler(pre_checkout)
    dp.register_message_handler(successful_pay, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(gpt_answer)