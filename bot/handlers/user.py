import logging
import os

import openai
from aiogram import types, Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from bot.database import add_subscription, check_subscription
from bot.database.user import get_subscription_end_date, get_requests

router = Router()


async def start_command(message: types.Message) -> types.Message:
    return await message.answer('Start')


async def buy_command(message: types.Message) -> types.Message:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Buy',
        callback_data='buy')
    )
    return await message.answer('Подписка на 1 месяц\n\nПлатная подписка позволит вам отправлять неограниченное число '
                         'запросов в течение 1 месяца\n\nЦена: 499.00р / месяц', reply_markup=builder.as_markup())


async def buy_send_invoice(callback: types.CallbackQuery) -> None:
    await callback.message.answer_invoice(
        title='Подписка на месяц',
        description='Платная подписка на ChatGPT бота даст вам возможность отправлять неограниченное число запросов в '
                    'течение 1 месяца',
        payload='month_sub',
        provider_token=os.getenv('payments_provider_token'),
        currency='RUB',
        start_parameter='',
        prices=[{'label': 'руб', 'amount': 49900}],
    )


async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(
        ok=True,
        error_message=''
    )


async def successful_pay(message: types.Message, session_maker: sessionmaker) -> None:
    if message.successful_payment.invoice_payload == 'month_sub':
        await message.answer('Вы успешно приобрели подписку!')
        await add_subscription(user_id=message.chat.id, session_maker=session_maker)


async def profile_command(message: types.Message, session_maker: sessionmaker) -> None:
    if await check_subscription(user_id=message.chat.id, session_maker=session_maker):
        end_date = await get_subscription_end_date(user_id=message.from_user.id, session_maker=session_maker)
        await message.answer(f'Профиль\n\nid: {message.chat.id}\nПодписка: есть\nОкончаниe подписки: {end_date}')
    else:
        requests = await get_requests(user_id=message.from_user.id, session_maker=session_maker)
        await message.answer(f'Профиль\n\nid: {message.chat.id}\nПодписка: нет\nЗапросы:  {requests}/{10}')


async def gpt_response(message: types.Message) -> None:
    openai.api_key = os.getenv('opneai_token_api')
    response = openai.ChatCompletion.create(
        # model="text-davinci-003",
        model="gpt-3.5-turbo",
        messages=[{'role': 'user', 'content': message.text}]
    )
    await message.answer(response['choices'][0]['message']['content'])
    logging.info(response)


def register_user_handlers(router: Router) -> None:
    router.message.register(start_command, Command(commands=['start']), flags={'registration_check': 'registration_check'})
    router.message.register(profile_command, Command(commands=['profile']))
    router.message.register(buy_command, Command(commands=['buy']))
    router.callback_query.register(buy_send_invoice, Text('buy'))
    router.pre_checkout_query.register(pre_checkout)
    router.message.register(successful_pay, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    router.message.register(gpt_response, flags={'update_requests': 'update_requests'})
