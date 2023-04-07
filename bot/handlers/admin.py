from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from bot.database import get_user_number, get_user_number_with_subscription


class AdminAnswer(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_message = State()


async def statistics_command(message: types.Message, session_maker: sessionmaker) -> None:
    users = await get_user_number(session_maker=session_maker)
    users_with_subscription = await get_user_number_with_subscription(session_maker=session_maker)
    await message.answer(
        f'Статистика по пользователям\n\nКоличество пользователей: {users}'
        f'\nКоличество подписчиков: {users_with_subscription}')


async def answer_command(message: types.Message, state: FSMContext) -> None:
    await message.answer('Введите id пользователя для ответа')
    await state.set_state(AdminAnswer.waiting_for_user_id)


async def set_user_id(message: types.Message, state: FSMContext) -> None:
    await state.update_data(user_id=message.text)
    await message.answer('Введите ответ для пользователя')
    await state.set_state(AdminAnswer.waiting_for_message)


async def set_message(message: types.Message, bot: Bot, state: FSMContext) -> None:
    await state.update_data(answer=message.text)
    user_data = await state.get_data()
    await message.answer('Ваш ответ направлен пользователю!')
    await bot.send_message(user_data['user_id'], f"На ваше обращение поступил ответ!\n\n{user_data['answer']}")
    await state.clear()
