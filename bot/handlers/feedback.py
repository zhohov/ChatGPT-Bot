import os

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class Feedback(StatesGroup):
    waiting_for_message = State()


async def feedback(message: types.Message, state: FSMContext) -> None:
    await message.answer('Оставьте свой вопрос здесь. Наши администраторы ответят вам в кратчайшие сроки')
    await state.set_state(Feedback.waiting_for_message)


async def feedback_message(message: types.Message, bot: Bot, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    user_data = await state.get_data()
    await message.answer('Спасибо за вопрос! Сообщение уже направлено администратору')
    await bot.send_message(os.getenv('admin_id'), f"Новый вопрос от пользователя: "
                                                  f"{message.from_user.id}\n\n{user_data['text']}")
    await state.clear()
