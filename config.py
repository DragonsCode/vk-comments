from runtime_config import required_env
from vkbottle import API, BuiltinStateDispenser, User
from vkbottle.bot import BotLabeler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


token = required_env('VK_BOT_TOKEN')
user_token = required_env('VK_USER_TOKEN')

api = API(token)
vk_user = User(token=user_token)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
scheduler = AsyncIOScheduler()

ADMIN_IDS = [549425694, 282952551, 85381166]
