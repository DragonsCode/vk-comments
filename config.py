from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


token = 'vk1.a.c_8cOaawjgcTkTFwmYtRpvJfQ6m09io0ru8EPxiQVt7FJR4lf-5XBgCCRiryyE2yAwtZ6rtd8l4XZG1FGgdoeXECTQgcENbxeXSlgau6GGHAo7uiPGlAePf_scriC-UQRbVsDa8Pr-2xrUL1gV8uJKkPy_Vov6LW0nWeY5MnJfMPNC1gNGdEqXuOOjzMhBlbupjzqC9y2LdNIJfoco5s7A'

api = API(token)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
scheduler = AsyncIOScheduler()