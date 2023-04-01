import datetime

from sqlalchemy import Column, Integer, TEXT, DATE, select, update
from sqlalchemy.orm import sessionmaker

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    # telegram user id
    user_id = Column(Integer, primary_key=True, nullable=False)
    # telegram username
    username = Column(TEXT, nullable=True)
    # user registration date
    register_date = Column(DATE, default=datetime.datetime.today())
    # number of user requests
    requests = Column(Integer, default=0)
    subscription = Column(Integer, default=0)
    subscription_end_date = Column(Integer, default=0)

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()


async def check_unique_user(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .where(User.user_id == user_id)
            )
            user = result.one_or_none()

            return False if user is not None else True


async def create_user(user_id: int, username: str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username,
            )
            session.add(user)


async def checking_the_number_of_requests(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            requests = await session.execute(
                select(User.requests)
                .where(User.user_id == user_id)
            )
            requests = requests.one_or_none()
            return False if requests[0] > 10 else True


async def update_requests(user_id: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(requests=User.requests + 1)
            )


async def check_subscription(user_id: int, session_maker: sessionmaker):
    pass
