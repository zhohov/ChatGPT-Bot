import logging
import os

import openai
from aiogram import types
from sqlalchemy.orm import sessionmaker

from bot.database import check_user_settings, get_user_openai_key, get_user_max_tokens


async def gpt_response(message: types.Message, session_maker: sessionmaker) -> None:
    if await check_user_settings(user_id=message.from_user.id, session_maker=session_maker):
        openai.api_key = await get_user_openai_key(user_id=message.from_user.id, session_maker=session_maker)
        max_tokens = await get_user_max_tokens(user_id=message.from_user.id, session_maker=session_maker)
    else:
        openai.api_key = os.getenv('opneai_token_api')
        max_tokens = 1000
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{'role': 'user', 'content': message.text}],
            max_tokens=max_tokens
        )
        await message.answer(response['choices'][0]['message']['content'])
        logging.info(response)
    finally:
        await message.answer('К сожалению, произошла ошибка.\nЕсли вы используете свой ключ, проверьте его')
