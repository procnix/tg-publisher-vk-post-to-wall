from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import kb_inline

router = Router()

START_WELCOME="""
Я бот, который умеет делать отложенные посты из телеграм в ВК!
Для того, чтобы начать, выбери нужное действие. 
"""

HELP_COMMAND="""
/start - запуск бота
/help - помощь по командам
"""

@router.message(Command('start'))
async def command_start(message: Message):
    menu = kb_inline.kb_builder()
    await message.answer(f'Привет <b>{message.from_user.username}!</b>{START_WELCOME}', 
                        parse_mode='html', reply_markup=menu)
    await message.delete()

@router.message(Command('help'))
async def command_help(message: Message):
    await message.answer(f'<b>{HELP_COMMAND}</b>', parse_mode='html')
    await message.delete()