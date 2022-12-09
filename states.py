from vkbottle import CtxStorage, BaseStateGroup

ctx = CtxStorage()

class PostData(BaseStateGroup):

    COUNT = 0
    LINK = 1


class DatingData(BaseStateGroup):

    WHAT = 0
    BACK = 1