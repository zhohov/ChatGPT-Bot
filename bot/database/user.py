import datetime

from sqlalchemy import Column, Integer, TEXT, DATE

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