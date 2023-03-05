from aiogram import Bot, Dispatcher
import openai
import os

openai.api_key = os.environ['opneai_api']
token_api = os.environ['token']
payments_token = os.environ['payments_token']
bot = Bot(token_api)
dp = Dispatcher(bot)