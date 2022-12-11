from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


token = 'vk1.a.PdBxBthx3qG98nynYuoZb1fs0ns80iF_KAOfQDpAgIBQMD1zuC6iBheqpWH0YdoiwGkBeTzCoaiQS_xZmCcw5M_e7R7eiFdhquoceizjJdOYC7JzJaeZEn5Xn5ZgiRJnUht__phyFcRVViif9bDAbt9Q1YBKRZTi6CiWMPAg-EkY0FyD8qGV73ZRnvdkT3_N'

api = API(token)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
scheduler = AsyncIOScheduler()

ADMIN_IDS = [549425694]