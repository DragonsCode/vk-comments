from vkbottle import API, BuiltinStateDispenser, User
from vkbottle.bot import BotLabeler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


token = 'vk1.a.c_8cOaawjgcTkTFwmYtRpvJfQ6m09io0ru8EPxiQVt7FJR4lf-5XBgCCRiryyE2yAwtZ6rtd8l4XZG1FGgdoeXECTQgcENbxeXSlgau6GGHAo7uiPGlAePf_scriC-UQRbVsDa8Pr-2xrUL1gV8uJKkPy_Vov6LW0nWeY5MnJfMPNC1gNGdEqXuOOjzMhBlbupjzqC9y2LdNIJfoco5s7A'
user_token = 'vk1.a.gcSKluVuVTJrMj9iDufKswZmrpFBuDSleTehyZRH8EDCrZZjMEvVdRgCDqQOi9jTOiF-96PnnXpOWI7sRr4EDRQA1ENqE0vl-str10CuNzOm1r6AyOv36bAszD7bPJA-EQQUp9cHGj4hrw7qeNH9IRcqlcE0cOxTo-Yp3AcAXLZAcG6PO8P2IaK4JZAjtVJtv_GeCl5Oie_JjtlilcbL2g'

api = API(token)
vk_user = User(token=user_token)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
scheduler = AsyncIOScheduler()

ADMIN_IDS = [549425694, 282952551, 85381166]
