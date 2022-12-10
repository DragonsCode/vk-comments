from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text

import asyncio

from models.db_api import methods as db
from config import api, state_dispenser
from states import DatingData, ctx
from comments import get_comment

read_post_labeler = BotLabeler()
read_post_labeler.vbml_ignore_case = True
read_post_labeler.auto_rules = [rules.PeerRule(from_chat=False)]

@read_post_labeler.message(text=['Читать посты'])
# @read_post_labeler.message(state=DatingData.BACK)
async def read_posts(message: Message):
    posts = db.get_dating_posts(message.peer_id)
    await state_dispenser.set(message.peer_id, DatingData.WHAT)
    if not posts:
        await state_dispenser.delete(message.peer_id)
        ctx.set(message.peer_id, {})

        keyboard = Keyboard(one_time=True)
        keyboard.add(Text('Читать посты'))
        keyboard.add(Text('Добавить пост'))
        
        await message.answer('☹️Все доступные для оценки посты разобрали\n\n💡Вернитесь немного позже', keyboard=keyboard)

    else:
        ctx.set(message.peer_id, {})
        data = ctx.get(message.peer_id)
        data['post_id'] = int(posts[0].id)
        data['post_link'] = posts[0].link
        ctx.set(message.peer_id, data)

        keyboard = Keyboard()
        keyboard.add(Text('Проверить'))
        keyboard.add(Text('Пропустить'))

        keyboard.row()
        keyboard.add(Text('Закончить'))

        await message.answer(f'📖Внимательно прочтите и напишите развернутый комментарий к данному посту:\n\n👉 {posts[0].link}', keyboard=keyboard)

@read_post_labeler.message(state=DatingData.WHAT)
async def watch_post(message: Message):
    if message.text == 'Проверить':
        user = await api.users.get(message.from_id)
        data = ctx.get(message.peer_id)
        url = data['post_link']
        fullname = f'{user[0].first_name} {user[0].last_name}'
        ok, comm = get_comment(fullname, url)
        print(comm)
        if not ok:
            await message.answer('☹️Не вижу вашего комментария под указанным постом\n\n💡Если вы оставили комментарий, но происходит ошибка - стоит подождать пару минут, и попробовать снова')
        else:
            if len(comm) > 10:
                db.change_balance(message.peer_id, 8)
                user = db.get_user_by_id(message.peer_id)
                db.insert_view(message.peer_id, data['post_id'])
                db.change_tasks(message.peer_id, 1)
                db.change_count(data['post_id'], -1)

                post = db.get_post_by_id(id=data['post_id'])
                if post.count <= 0:
                    db.delete_post(post.id)
                    db.delete_view(post.id)
                    await api.messages.send(peer_id=post.user_id, message=f'Работа над вашим постом {post.link} была завершена, получено {post.comms}💬', random_id=0)
                
                await message.answer(f'✅Отлично! За выполнение задания вам начислено 8 балла\n\n💡У вас: {user.balance} баллов')
                await api.messages.set_activity(type='typing', peer_id=message.peer_id)
                await asyncio.sleep(2)
                await read_posts(message)
            else:
                await message.answer('👀Ваш комментарий слишком короткий\n\n💡Старайтесь писать комментарии развернуто, так, бот точно зачтет труды')
    

    if message.text == 'Пропустить':
        data = ctx.get(message.peer_id)
        user = db.get_user_by_id(message.peer_id)
        if user.skips <= 0:
            await message.answer('🤔За сегодня вы пропустили слишком много постов\n\n💡Подождите, или напишите мнение к текущему посту')
        else:
            db.change_skips(message.peer_id, -1)
            db.insert_view(message.peer_id, data['post_id'])
            await api.messages.set_activity(type='typing', peer_id=message.peer_id)
            await asyncio.sleep(2)
            await read_posts(message)
    

    if message.text == 'Закончить':
        await state_dispenser.delete(message.peer_id)
        ctx.set(message.peer_id, {})

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
                text += "\n"+b + f' – {i.all-i.count} 💬 из ' + f'{i.all} 💬'
        await message.answer(text, keyboard=keyboard)