from config import scheduler, api
from models.db_api import methods as db


async def get_bonus():
    users = db.get_user_by_id()
    for user in users:
        a = 0 if user.skips == 3 else 1 if user.skips == 2 else 2 if user.skips == 1 else 3 if user.skips == 0 else 0
        db.change_skips(user.user_id, a)
        # await api.messages.send(peer_id=user.user_id, message='You got free skips', random_id=0)

def bonus_schedule():
    scheduler.add_job(get_bonus, 'interval', days=1)