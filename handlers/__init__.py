from .activate import activate_labeler
from .read_posts import read_post_labeler
from .add_post import add_post_labeler
from .admin import admin_labeler
# Если использовать глобальный лейблер, то все хендлеры будут зарегистрированы в том же порядке, в котором они были импортированы

__all__ = ("activate_labeler", "read_post_labeler", "add_post_labeler", "admin_labeler")