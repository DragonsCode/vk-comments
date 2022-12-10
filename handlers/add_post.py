from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text

from models.db_api import methods as db
from config import api, state_dispenser
from states import PostData, ctx
from comments import get_post

add_post_labeler = BotLabeler()
add_post_labeler.vbml_ignore_case = True
add_post_labeler.auto_rules = [rules.PeerRule(from_chat=False)]

@add_post_labeler.message(text=['Добавить пост'])
async def add_post(message: Message):
    user = db.get_user_by_id(user_id=message.peer_id)
    if user.balance > 10:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('5'))
        keyboard.add(Text('10'))
        keyboard.add(Text('20'))

        ctx.set(message.peer_id, {})
        await state_dispenser.set(message.peer_id, PostData.COUNT)

        await message.answer(
            '❓Какое число комментариев вы желаете получить? Введите число или выберите из предложенных вариантов\n\n💡Один комментарий стоит 10 баллов',
            keyboard=keyboard
        )
    else:
        await message.answer('☹️Чтобы добавить пост, необходимо заработать баллы\n\n💡Сделайте это в "Читать посты"!')

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


@add_post_labeler.message(state=PostData.COUNT)
async def post_count(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        user = db.get_user_by_id(user_id=message.peer_id)
        if user.balance >= int(message.text)*10:
            data = ctx.get(message.peer_id)
            data['count'] = int(message.text)
            ctx.set(message.peer_id, data)
            await state_dispenser.set(message.peer_id, PostData.LINK, count=message.text)
            await message.answer('📝Введите, пожалуйста, ссылку на пост\n\n💡Вы можете запрашивать комментарии поста только на свою страницу. Или же, на пост любого доступного сообщества')
        else:
            await message.answer(f'☹️На такое число комментариев не хватает баллов\n\n💡Сейчас у вас: {user.balance} баллов, необходимо: {int(message.text)*10-user.balance} баллов')
    else:
        await message.answer('☹️Пожалуйста, введите число')

@add_post_labeler.message(state=PostData.LINK)
async def post_link(message: Message):
    data = ctx.get(message.peer_id)
    count = data['count']
    link = message.text

    ok, msg = get_post(link)
    if not ok:
        if msg == 'Old post':
            await message.answer('☹️Этот пост не подойдет\n🕛Я принимаю только записи, существующие менее двух суток')
        else:
            await message.answer('☹️Пожалуйста, пришлите ссылку на пост сообщества или пост с вашего аккаунта')
    else:
        if msg == 'user' and message.peer_id != int(link.split('wall')[1].split('_')[0]):
            await message.answer('☹️Вы можете запрашивать комментарии только на страницу исполнения или же любое сообщество')
        else:
            bal = -10*count
            db.insert_post(message.peer_id, link, count)
            db.change_balance(message.peer_id, bal)
            posts = db.get_post_by_id(user_id=message.peer_id)
            db.insert_view(message.peer_id, posts[-1].id)
            await message.answer('✅Отлично, пост добавлен в список комментирования!\n\n💡Я сообщу, когда наберется нужное число комментариев')

            await state_dispenser.delete(message.peer_id)
            ctx.set(message.peer_id, {})

            user = db.get_user_by_id(user_id=message.peer_id)

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

