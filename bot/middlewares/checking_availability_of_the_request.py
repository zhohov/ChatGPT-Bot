from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from bot.database import (
    checking_the_number_of_requests,
    update_requests, check_subscription,
    checking_subscription_availability,
    deleting_subscription, check_user_settings
)


class RequestsCheck(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        flag = get_flag(data, 'update_requests')

        session_maker = data['session_maker']
        if not flag:
            return await handler(event, data)
        else:
            await data['bot'].send_message(event.from_user.id, 'Формируем ответ...')
            async with ChatActionSender(chat_id=event.chat.id, action='typing', interval=5.0, initial_sleep=0.0):
                if await check_subscription(user_id=event.from_user.id, session_maker=session_maker) \
                            or await check_user_settings(user_id=event.from_user.id, session_maker=session_maker):
                    if await checking_subscription_availability(user_id=event.from_user.id, session_maker=session_maker) \
                            or await check_user_settings(user_id=event.from_user.id, session_maker=session_maker):
                        return await handler(event, data)
                    else:
                        await deleting_subscription(user_id=event.from_user.id, session_maker=session_maker)
                        await data['bot'].send_message(event.from_user.id,
                                                       'К сожалению ваша подписка закончилась(\n\nВы '
                                                       'можете оплатить ее снова, либо '
                                                       'воспользоваться бесплатными запросами')
                elif await checking_the_number_of_requests(user_id=event.from_user.id, session_maker=session_maker):
                    await update_requests(user_id=event.from_user.id, session_maker=session_maker)
                    return await handler(event, data)
                else:
                    await data['bot'].send_message(event.from_user.id, 'Вы превысили количество запросов')
