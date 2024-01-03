import datetime
from aiogram import F
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup
from keyboards import kb_inline
from db.db_interval import create_table, delay_post_table, get_time_interval, set_time_interval
from vk_back.post.send import send_post, delay_post

router = Router()

user_states = {}

# Создаем таблицу в базе данных, если её нет
create_table()


@router.callback_query(F.data == 'send_now')
async def process_button(callback: CallbackQuery):
    await callback.message.answer(text='Пришли пост, который нужно опубликовать сейчас')
    user_id = callback.from_user.id
    user_states[user_id] = 'send_now'
    await callback.answer()


@router.message(F.text)
async def check_post(message: Message):
    user_id = message.from_user.id
    if user_id in user_states:
        if user_states[user_id] == 'send_now':
            await message.reply('Это не фото! Отправь мне картинку!')
        elif user_states[user_id] == 'add_to_deferred':
            await message.reply('Отправь мне картинку!')
        elif user_states[user_id] == 'time_post':
            print(message)
            await message.reply('Выбери интервал!')
        del user_states[user_id]
    else:
        menu = kb_inline.kb_builder()
        await message.reply('Ты прислал текс, а не выбрал действие!', reply_markup=menu)


@router.message(F.photo)
async def command_start(message: Message, bot: Bot):
    user_id = message.from_user.id
    if user_id in user_states:
        if user_states[user_id] == 'send_now':
            menu = kb_inline.kb_builder()
            file = await bot.get_file(message.photo[-1].file_id)
            photo = await bot.download_file(file.file_path)
            post_id = await send_post(photo)
            await message.delete()
            await message.answer(f"Пост <b>{post_id}</b> опубликован <b>{datetime.datetime.now().replace(microsecond=0)}</b>",
                                reply_markup=menu, parse_mode='html')
        elif user_states[user_id] == 'add_to_deferred':
            menu = kb_inline.kb_builder()
            file = await bot.get_file(message.photo[-1].file_id)
            photo = await bot.download_file(file.file_path)
            post_id = await delay_post(photo, user_id)
            await message.answer(f"Пост <b>{post_id['post']}</b> добавлен в отложку <b>{datetime.datetime.fromtimestamp(post_id['date'])}</b> ",
                                reply_markup=menu, parse_mode='html')
            await message.delete()
        del user_states[user_id]
    else:
        menu = kb_inline.kb_builder()
        await message.reply('Ты не выбрал действие!', reply_markup=menu)


@router.callback_query(F.data == 'time_post')
async def choice_time(callback: CallbackQuery):
    user_id = callback.from_user.id
    time_interval = get_time_interval(user_id)

    menu = kb_inline.kb_time()

    for row in menu.inline_keyboard:
        for button in row:
            if button.callback_data == "-1":
                continue
            if time_interval == button.callback_data:
                button.text = f"[✅] {button.text[4:]}"
            else:
                button.text = f"[❌] {button.text[4:]}"
    
    updated_menu = InlineKeyboardMarkup(inline_keyboard=menu.inline_keyboard)
    
    if time_interval:
        await callback.message.edit_text(text='Интервал уже выбран!', reply_markup=updated_menu)
        await callback.answer()
    else:
        await callback.message.edit_text(text='Сейчас интервал не задан! Выбери интервал публикации постов',
                                        reply_markup=menu)
        await callback.answer()


@router.callback_query(F.data.in_(['1', '2', '3', '4', '-1']))
async def set_interval(callback: CallbackQuery):
    user_id = callback.from_user.id
    time_interval = callback.data
    if time_interval == '-1':
        await back_menu(callback)
    else:
        set_time_interval(user_id, time_interval)
        await choice_time(callback)

async def back_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_states[user_id] = '-1'
    menu = kb_inline.kb_builder()
    await callback.message.edit_text(text=f'Привет <b>{callback.from_user.username}!</b> Выбери действие', 
                                    reply_markup=menu, parse_mode='html')
    await callback.answer()


@router.callback_query(F.data == 'add_to_deferred')
async def add_time_in_post(callback: CallbackQuery):
    await callback.message.answer(text='Пришли пост, который нужно добавить в отложку')
    user_id = callback.from_user.id
    user_states[user_id] = 'add_to_deferred'
    await callback.answer()
