__all__ = [
    'register_start_handlers',
    'register_profile_handlers',
    'register_buy_handlers',
    'register_admin_handlers',
    'register_response_handlers',
    'bot_commands'
]

from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.filters import Command, Text

from .profile import profile_command, edit_api_key, set_new_api_key, edit_max_tokens, set_new_max_tokens, remove_token, \
    UpdateApiKey, UpdateMaxTokens
from .start import start_command, cancel_command, settings_command, waiting_api_key, waiting_max_tokens, ApiSettings, \
    max_tokens_incorrect, about_command
from .buy import buy_command, buy_send_invoice, pre_checkout, successful_pay
from .gptresponse import gpt_response
from .admin import statistics_command
from .bot_commands import bot_commands


def register_start_handlers(router: Router) -> None:
    router.message.register(start_command, Command(commands=['start']), flags={'registration_check': 'registration_check'})
    router.message.register(about_command, Command(commands=['about']))
    router.message.register(cancel_command, Command(commands=['cancel']))
    router.message.register(settings_command, Command(commands=['settings']))
    router.message.register(waiting_api_key, ApiSettings.waiting_for_api_key)
    router.message.register(waiting_max_tokens, ApiSettings.waiting_for_max_tokens,
                            lambda message: message.text.isdigit() and int(message.text) <= 4096)
    router.message.register(max_tokens_incorrect, ApiSettings.waiting_for_max_tokens)


def register_buy_handlers(router: Router) -> None:
    router.message.register(buy_command, Command(commands=['buy']))
    router.callback_query.register(buy_send_invoice, Text('buy'))
    router.pre_checkout_query.register(pre_checkout)
    router.message.register(successful_pay, F.content_type == ContentType.SUCCESSFUL_PAYMENT)


def register_profile_handlers(router: Router) -> None:
    router.message.register(profile_command, Command(commands=['profile']))
    router.callback_query.register(edit_api_key, Text('api_key'))
    router.message.register(set_new_api_key, UpdateApiKey.waiting_api_key)
    router.callback_query.register(edit_max_tokens, Text('max_tokens'))
    router.message.register(set_new_max_tokens, UpdateMaxTokens.waiting_max_tokens,
                            lambda message: message.text.isdigit() and int(message.text) <= 4096)
    router.message.register(max_tokens_incorrect, UpdateMaxTokens.waiting_max_tokens)
    router.callback_query.register(remove_token, Text('remove_token'))


def register_admin_handlers(router: Router) -> None:
    router.message.register(statistics_command, Command(commands=['statistics']), flags={'admin_check': 'admin_check'})


def register_response_handlers(router: Router) -> None:
    router.message.register(gpt_response, flags={'update_requests': 'update_requests'})
