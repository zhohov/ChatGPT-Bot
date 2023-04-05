from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from bot.database import set_user_settings


class ApiSettings(StatesGroup):
    waiting_for_api_key = State()
    waiting_for_max_tokens = State()


async def start_command(message: types.Message) -> types.Message:
    return await message.answer('Start')


async def cancel_command(message: types.Message, state: FSMContext) -> types.Message:
    await state.clear()
    return await message.answer('Действие отменено')


async def settings_command(message: types.Message, state: FSMContext) -> None:
    await message.answer('Настройки\nВведите свой апи ключ')
    await state.set_state(ApiSettings.waiting_for_api_key)


async def waiting_api_key(message: types.Message, state: FSMContext) -> None:
    await state.update_data(api_key=message.text)
    await message.answer('Введите максимальное количество токенов для ответа (1 символ ~ 1 токен), максимум - 4096')
    await state.set_state(ApiSettings.waiting_for_max_tokens)


async def waiting_max_tokens(message: types.Message, state: FSMContext, session_maker: sessionmaker) -> None:
    await state.update_data(max_tokens=message.text)
    user_data = await state.get_data()
    await set_user_settings(
        user_id=message.from_user.id,
        api_key=user_data['api_key'],
        max_tokens=int(user_data['max_tokens']),
        session_maker=session_maker
    )
    await message.answer(f"Вы успешно настроили доступ к ChatGPT:\nВаш апи ключ: {user_data['api_key']}"
                         f"\nмаксимальное количество токенов: {user_data['max_tokens']}")
    await state.clear()


async def max_tokens_incorrect(message: types.Message) -> types.Message:
    return await message.answer('Введено некорректное значение!\nМаксимальное количество токенов для ответа'
                                ' должно быть цифрой, которая меньше 4096\nПовторите попытку')
