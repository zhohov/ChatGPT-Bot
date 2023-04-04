import logging
import os
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message


class AdminCheck(BaseMiddleware):
    async def __call__(
             self,
             handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
             event: Message,
             data: Dict[str, Any],
    ) -> Any:
        flag = get_flag(data, 'admin_check')

        if not flag:
            return await handler(event, data)
        else:
            if event.from_user.id == int(os.getenv('admin_id')):
                logging.info('Using admin panel')
                return await handler(event, data)
            else:
                logging.info("User is not admin")
                await data['bot'].send_message(event.from_user.id, 'У вас недостаточно прав для использования этой команды')
