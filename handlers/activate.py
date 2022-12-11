from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text

import asyncio

from models.db_api import methods as db
from config import api

activate_labeler = BotLabeler()
activate_labeler.vbml_ignore_case = True
activate_labeler.auto_rules = [rules.PeerRule(from_chat=False)]



@activate_labeler.message(text=['Принимаю'])
@activate_labeler.message(payload={'cmd': 'agree'})
async def agree(message: Message):
    await api.messages.set_activity(type='typing', peer_id=message.peer_id)
    await asyncio.sleep(2)
    await message.answer('✅Вы успешно зарегистрированы')

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
                b = await api.utils.get_short_link(i.link)
                b = b.short_url
            except:
                b = i.link
            text += "\n"+b + f' – {i.comms-i.count} 💬 из ' + f'{i.comms} 💬'
    await message.answer(text, keyboard=keyboard)