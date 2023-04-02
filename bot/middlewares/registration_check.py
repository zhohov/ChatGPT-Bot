import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message

from bot.database import check_unique_user, create_user


class RegistrationCheck(BaseMiddleware):
    async def __call__(
             self,
             handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
             event: Message,
             data: Dict[str, Any],
    ) -> Any:
        flag = get_flag(data, 'registration_check')

        session_maker = data['session_maker']

        if not flag:
            return await handler(event, data)
        else:
            if await check_unique_user(user_id=event.from_user.id, session_maker=session_maker):
                await create_user(
                    user_id=event.from_user.id,
                    username=event.from_user.username,
                    session_maker=session_maker,
                )
                logging.info('A new user has been registered')
            else:
                logging.info("User has been registered")

            return await handler(event, data)
