import os

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from bot.database import add_subscription


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
