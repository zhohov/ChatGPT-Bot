import os

from aiogram import types, Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


async def start_command(message: types.Message) -> Message:
    return await message.answer('Start')


async def request_command(message: types.Message) -> Message:
    return await message.answer('Request!')


async def buy_command(message: types.Message) -> None:
    await message.answer('Подписка на 1 месяц\n\nПлатная подписка позволит вам отправлять неограниченное число '
                         'запросов в течение 1 месяца\n\nЦена: 499.00р / месяц')
    await message.answer_invoice(
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


async def successful_pay(message: types.Message) -> Message:
    if message.successful_payment.invoice_payload == 'month_sub':
        return await message.answer('Вы успешно приобрели подписку!')


def register_user_handlers(router: Router) -> None:
    router.message.register(start_command, Command(commands=['start']), flags={'registration_check': 'registration_check'})
    router.message.register(request_command, Command(commands=['request']), flags={'update_requests': 'update_requests'})
    router.message.register(buy_command, Command(commands=['buy']))
    router.pre_checkout_query.register(pre_checkout)
    router.message.register(successful_pay, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
