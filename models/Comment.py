from models import Model


class Comment(Model):
    user_id: int
    weibo_id: int
    content: str
