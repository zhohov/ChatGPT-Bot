from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from bot.database import check_subscription, get_subscription_end_date, get_requests, check_user_settings, \
    update_user_api_key, update_user_max_tokens


class UpdateApiKey(StatesGroup):
    waiting_api_key = State()


class UpdateMaxTokens(StatesGroup):
    waiting_max_tokens = State()


async def profile_command(message: types.Message, session_maker: sessionmaker) -> types.Message:
    if await check_subscription(user_id=message.chat.id, session_maker=session_maker):
        end_date = await get_subscription_end_date(user_id=message.from_user.id, session_maker=session_maker)
        return await message.answer(f'Профиль\n\nid: {message.chat.id}\nПодписка: есть\nОкончаниe подписки: {end_date}')
    elif await check_user_settings(user_id=message.from_user.id, session_maker=session_maker):
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(text='api key', callback_data='api_key'),
            types.InlineKeyboardButton(text='max tokens', callback_data='max_tokens'),
            types.InlineKeyboardButton(text='remove token', callback_data='remove_token')
        )
        return await message.answer(f'Профиль\n\nid: {message.chat.id}\nДля ответов вы используете свой токен'
                                    f'\nДля настройки бота используйте кнопки ниже', reply_markup=builder.as_markup())
    else:
        requests = await get_requests(user_id=message.from_user.id, session_maker=session_maker)
        return await message.answer(f'Профиль\n\nid: {message.chat.id}\nПодписка: нет\nЗапросы:  {requests}/{10}')


async def edit_api_key(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer('Введите новый апи ключ')
    await state.set_state(UpdateApiKey.waiting_api_key)


async def set_new_api_key(message: types.Message, state: FSMContext, session_maker: sessionmaker) -> None:
    await state.update_data(api_key=message.text)
    user_data = await state.get_data()
    await update_user_api_key(user_id=message.from_user.id, api_key=user_data['api_key'], session_maker=session_maker)
    await message.answer('Ваш ключ успешно изменен!')
    await state.clear()


async def edit_max_tokens(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer('Введите новое значения для максимального количество токенов для ответа')
    await state.set_state(UpdateMaxTokens.waiting_max_tokens)


async def set_new_max_tokens(message: types.Message, state: FSMContext, session_maker: sessionmaker) -> None:
    await state.update_data(max_tokens=message.text)
    user_data = await state.get_data()
    await update_user_max_tokens(user_id=message.from_user.id, max_tokens=int(user_data['max_tokens']), session_maker=session_maker)
    await message.answer('Максимальное количество токенов успешно установлено')
    await state.clear()


async def max_tokens_incorrect(message: types.Message) -> types.Message:
    return await message.answer('Введено некорректное значение!\nМаксимальное количество токенов для ответа'
                                ' должно быть цифрой, которая меньше 4096\nПовторите попытку')


async def remove_token(callback: types.CallbackQuery) -> None:
    await callback.message.answer('Ваш токен удален!\nВы по прежнему можете пользоваться бесплатными запросами или '
                                  'купить подписку на месяц')
