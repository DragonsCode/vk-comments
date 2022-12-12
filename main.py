# coding=utf8
from vkbottle import Keyboard, Text
from vkbottle.bot import Message
from vkbottle import Bot

import asyncio

from models.db_api import dbms
from models.db_api import methods as db
from config import api, state_dispenser, labeler, scheduler
from handlers import activate_labeler, read_post_labeler, add_post_labeler, admin_labeler
from tasks.bonus import bonus_schedule


labeler.load(activate_labeler)
labeler.load(read_post_labeler)
labeler.load(add_post_labeler)
labeler.load(admin_labeler)

scheduler.start()

bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)

@bot.on.private_message(text=['Hello <name>', 'Hello'])
async def hello(message: Message, name=None):
    if name is not None:
        await message.answer(f'Hello to {name}')
    else:
        user = await bot.api.users.get(message.from_id)
        await message.answer(f'Hello {user[0].first_name} {user[0].last_name}')

@bot.on.private_message()
async def chat(message: Message):
    a = db.insert_user(message.peer_id)
    if a:
        user = db.get_user_by_id(user_id=message.peer_id)
        posts = db.get_post_by_id(user_id=message.peer_id)

        keyboard = Keyboard(one_time=True)
        keyboard.add(Text('Читать посты'))
        keyboard.add(Text('Добавить пост'))

        text = str(user)+f'\n💼Добавлено постов: {len(posts)}'+f'\n👀Оценено постов: {user.tasks}'
        if len(posts) != 0:
            text += '\n\n🌐Посты в работе:'
            for i in posts:
                b = i.link
                try:
                    b = await bot.api.utils.get_short_link(i.link)
                    b = b.short_url
                except:
                    b = i.link
                text += "\n"+b + f' – {i.comms-i.count} 💬 из ' + f'{i.comms} 💬'
        await message.answer(text, keyboard=keyboard)
        return
    
    await message.answer('👋Привет! Я бот по кросспиару')
    keyboard = Keyboard(inline=True)
    keyboard.add(Text('Принимаю', {'cmd': 'agree'}))
    await bot.api.messages.set_activity(type='typing', peer_id=message.peer_id)
    await asyncio.sleep(1.5)
    await message.answer('❗Пожалуйста, ознакомьтесь с правилами:\n- Внимательно читайте предложенные посты\n- Пишите свое мнение в комментариях, не менее 10 символов\n- Публикацию проходят посты, опубликованные ранее 48 часов\n- За публикацию постов запрещенных тематик -> вечный бан\n- Мы не несем ответственность за содержание постов пользователей.', keyboard=keyboard)



def run_main():
    # Create Tables
    dbms.create_db_tables()
    bonus_schedule()

run_main()

#bot.labeler.message_view.register_middleware(InfoMiddleware)

bot.run_forever()