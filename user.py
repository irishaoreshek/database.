#import database.database as dtb
import requests

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from lexicon.lexicon import LEXICON
from servises.servises import random_number
from config_data.config import Config, load_config
from database.database import addUser, addHistory, SelectOneUser, UpdateUser, isFindUser, FirstFiveUsers, updateKD, stringKD

config: Config = load_config('\.env')

async def start_message(msg: Message):
    addUser(msg)
    await msg.answer(LEXICON["/start"])

async def help_message(msg: Message):
    await msg.answer(LEXICON['/help'])

async def statistik_user(msg: Message):
    await msg.answer(f'Всего игры сыграно: {SelectOneUser(msg)[7]}\nИз них побед: {SelectOneUser(msg)[6]}')

async def cancel_game(msg: Message):
    if SelectOneUser(msg)[8]:
        await msg.answer(LEXICON["/cancel"])
        UpdateUser(msg, in_game=False)
    else:
        await msg.answer(LEXICON["not_in_game"])

async def global_statistics(msg: Message):
    await msg.answer(FirstFiveUsers(msg))

async def statistikAllGame(msg: Message):
    string = stringKD(msg)
    await msg.answer(f"{string}")

async def process_positive_answer(msg: Message):
    if not SelectOneUser(msg)[8]:
        await msg.answer(LEXICON["isnumber"])
        UpdateUser(msg, in_game=True, secret_number=random_number(1, 100), attempts=5)
    else:
        await msg.answer(LEXICON["in_game"])

async def procces_negative_answer(msg: Message):
    if SelectOneUser(msg)[8]:
        await msg.answer(LEXICON["in_game"])
    else:
        await msg.answer(LEXICON["negative_answer"])

async def process_numbers_answer(msg: Message):
    if SelectOneUser(msg)[8]:
        input_number = SelectOneUser(msg)[4]
        if int(msg.text) == input_number:
            updateKD(msg)
            addHistory(msg, iswin=1)
            await msg.answer(LEXICON["win"])
            cat_response = requests.get(config.cat.token)

            if cat_response.status_code == 200:
                cat_link = cat_response.json()['file']
                await msg.answer_photo(cat_link)
                await msg.answer(LEXICON["again"])
            else:
                await msg.answer(LEXICON["ERROR_TEXT"])
                await msg.answer(LEXICON["again"])
            
            UpdateUser(msg, in_game=False, 
                           total_games=SelectOneUser(msg)[7] + 1,
                           wins= SelectOneUser(msg)[6] + 1)
        
        elif int(msg.text) > input_number:
            await msg.answer(LEXICON["smalest"])
            UpdateUser(msg, attempts=SelectOneUser(msg)[5] - 1)
        
        elif int(msg.text) < input_number:
            await msg.answer(LEXICON["biggest"])
            UpdateUser(msg, attempts=SelectOneUser(msg)[5] - 1)

        if SelectOneUser(msg)[5] == 0:
            updateKD(msg)
            addHistory(msg, iswin=0)
            await msg.answer(f'Увы, игра окончена, вы проиграли, загаданное число {SelectOneUser(msg)[4]} :(\nХотите сыграть ещё раз?')
            UpdateUser(msg, in_game=False, 
                           total_games=SelectOneUser(msg)[7] + 1)
        
    else:
        await msg.answer(LEXICON["not_in_game"])
        
async def registrator(msg: Message):
    addUser(msg)

def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_message ,commands=["start"])
    dp.register_message_handler(help_message, commands=["help"])
    dp.register_message_handler(statistik_user, commands=["stat"])
    dp.register_message_handler(cancel_game, commands=["cancel"])
    dp.register_message_handler(global_statistics, commands=["global"])
    dp.register_message_handler(statistikAllGame, commands=['all'])
    dp.register_message_handler(process_positive_answer, Text(equals=['Да', 'Yes', 'Let\'s', 'Давай', 'Погнали', 'Start', 'Начать'], ignore_case=True))
    dp.register_message_handler(procces_negative_answer, Text(equals=['Нет', 'No', 'Я откажусь', 'Не', 'не хочу'], ignore_case=True))
    dp.register_message_handler(process_numbers_answer, lambda x: x.text.isdigit() and (1 <= int(x.text) <= 100))
    dp.register_message_handler(registrator, lambda x: isFindUser(x.from_user.id))
