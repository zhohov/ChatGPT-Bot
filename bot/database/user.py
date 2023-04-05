import datetime

from sqlalchemy import Column, Integer, TEXT, DATE, select, update, func
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
    # user key usage
    custom_key = Column(Integer, default=0)
    # user openai api key
    user_openai_key = Column(TEXT, default=' ')
    # user openai max_tokens for gpt response
    user_openai_max_tokens = Column(Integer, default=0)

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
            return False if requests[0] > 9 else True


async def update_requests(user_id: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(requests=User.requests + 1)
            )


async def add_subscription(user_id: int, session_maker: sessionmaker) -> None:
    start_subscription_date = datetime.datetime.today().replace(microsecond=0)
    timestamp_date = int(datetime.datetime.timestamp(start_subscription_date))
    timestamp_date += 60 * 60 * 24 * 30

    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(subscription_end_date=timestamp_date, subscription=1)
            )


async def check_subscription(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            subscription = await session.execute(
                select(User.subscription)
                .where(User.user_id == user_id)
            )
            subscription = subscription.one_or_none()
            return True if subscription[0] == 1 else False


async def checking_subscription_availability(user_id: int, session_maker: sessionmaker) -> bool:
    date = datetime.datetime.today().replace(microsecond=0)
    timestamp_date = int(datetime.datetime.timestamp(date))

    async with session_maker() as session:
        async with session.begin():
            subscription_end_date = await session.execute(
                select(User.subscription_end_date)
                .where(User.user_id == user_id)
            )
            subscription_end_date = subscription_end_date.one_or_none()
            return True if subscription_end_date[0] > timestamp_date else False


async def deleting_subscription(user_id: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(subscription_end_date=0, subscription=0, requests=0)
            )


# profile methods
async def get_requests(user_id: int, session_maker: sessionmaker) -> int:
    async with session_maker() as session:
        async with session.begin():
            requests = await session.execute(
                select(User.requests)
                .where(User.user_id == user_id)
            )
            requests = requests.one_or_none()
            return requests[0]


async def get_subscription_end_date(user_id: int, session_maker: sessionmaker) -> str:
    async with session_maker() as session:
        async with session.begin():
            date = await session.execute(
                select(User.subscription_end_date)
                .where(User.user_id == user_id)
            )
            date = date.one_or_none()
            date = datetime.datetime.fromtimestamp(date[0]).strftime("%b %d %Y - %H:%M:%S")
            return str(date)


# admin panel methods
async def get_user_number(session_maker: sessionmaker) -> int:
    async with session_maker() as session:
        async with session.begin():
            count = await session.scalar(select(func.count(User.user_id)))
            return count


async def get_user_number_with_subscription(session_maker: sessionmaker) -> int:
    async with session_maker() as session:
        async with session.begin():
            count = await session.scalar(
                select(func.count(User.user_id))
                .where(User.subscription == 1)
            )
            return count
