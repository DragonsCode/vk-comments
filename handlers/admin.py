from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text

from models.db_api import methods as db
from config import api, ADMIN_IDS

admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True
admin_labeler.auto_rules = [rules.PeerRule(from_chat=False)]

@admin_labeler.message(text=['addpoints <id> <bal>', 'addpoints'], peer_ids=ADMIN_IDS)
async def addpoints(message: Message, id=None, bal=None):
    if (id is None and bal is None) and not (id.isdigit() and bal.isdigit()):
        await message.answer('Используйте команду правильно: addpoints [vkid] [баллы]')
    else:
        id = int(id)
        if bal[0] == '-':
            await message.answer('Нельзя указывать отрицательное число')
            return
        bal = int(bal)
        user = db.get_user_by_id(user_id=id)
        if not user:
            await message.answer('Пользователь с таким ID в боте не найден')
            return
        db.change_balance(id, bal)
        user = await api.users.get(id)
        user_info = db.get_user_by_id(user_id=id)
        await api.messages.send(peer_id=id, message=f'📝Вам начислено {bal} баллов\n\n💡Текущий баланс: {user_info.balance} баллов', random_id=0)
        await message.answer(f'Теперь у [id{id}|{user[0].first_name} {user[0].last_name}] {user_info.balance} баллов.')

@admin_labeler.message(text=['delpoints <id> <bal>', 'delpoints'], peer_ids=ADMIN_IDS)
async def delpoints(message: Message, id=None, bal=None):
    if (id is None and bal is None) and not (id.isdigit() and bal.isdigit()):
        await message.answer('Используйте команду правильно: delpoints [vkid] [баллы]')
    else:
        id = int(id)
        if bal[0] == '-':
            await message.answer('Нельзя указывать отрицательное число')
            return
        bal = int(bal)
        user = db.get_user_by_id(user_id=id)
        if not user:
            await message.answer('Пользователь с таким ID в боте не найден')
            return
        if user.balance < bal:
            b = -user.balance
            db.change_balance(id, b)
        else:
            b = -bal
            db.change_balance(id, b)
        user_info = db.get_user_by_id(user_id=id)
        user = await api.users.get(id)
        await api.messages.send(peer_id=id, message=f'📝Вам снято {bal} баллов\n\n💡Текущий баланс: {user_info.balance} баллов', random_id=0)
        await message.answer(f'Теперь у [id{id}|{user[0].first_name} {user[0].last_name}] {user_info.balance} баллов.')

@admin_labeler.message(text=['checkuser <id>', 'checkuser'], peer_ids=ADMIN_IDS)
async def checkuser(message: Message, id=None):
    if id is None and not id.isdigit():
        await message.answer('Используйте команду правильно: checkuser [vkid]')
    else:
        id = int(id)
        user = db.get_user_by_id(user_id=id)
        if not user:
            await message.answer('Пользователь с таким ID в боте не найден')
            return
        posts = db.get_post_by_id(user_id=id)

        usr = await api.users.get(id)
        text = f'Данные профиля [id{id}|{usr[0].first_name} {usr[0].last_name}]:\n\n'+str(user)+f'\n💼Добавлено постов: {len(posts)}'+f'\n👀Оценено постов: {user.tasks}'
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
        await message.answer(text)