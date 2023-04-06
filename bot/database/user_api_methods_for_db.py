from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker

from .user import User


async def check_user_settings(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            settings = await session.execute(
                select(User.custom_key)
                .where(User.user_id == user_id)
            )
            settings = settings.one_or_none()
            return True if settings[0] == 1 else False


async def set_user_settings(user_id: int, api_key: int, max_tokens: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(custom_key=1, user_openai_key=api_key, user_openai_max_tokens=max_tokens)
            )


async def update_user_api_key(user_id: int, api_key: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(user_openai_key=api_key)
            )


async def update_user_max_tokens(user_id: int, max_tokens: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(user_openai_max_tokens=max_tokens)
            )


async def get_user_openai_key(user_id: int, session_maker: sessionmaker) -> str:
    async with session_maker() as session:
        async with session.begin():
            api_key = await session.execute(
                select(User.user_openai_key)
                .where(User.user_id == user_id)
            )
            api_key = api_key.one_or_none()
            return api_key[0]


async def get_user_max_tokens(user_id: int, session_maker: sessionmaker) -> int:
    async with session_maker() as session:
        async with session.begin():
            max_tokens = await session.execute(
                select(User.user_openai_max_tokens)
                .where(User.user_id == user_id)
            )
            max_tokens = max_tokens.one_or_none()
            return max_tokens[0]


async def remove_user_settings(user_id: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(custom_key=0, user_openai_key='None', user_openai_max_tokens=0)
            )
