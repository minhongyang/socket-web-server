import time

from models import Model
from utils import formatted_time


class Todo(Model):
    user_id: int
    task: str
    created_time: int
    updated_time: int

    @classmethod
    def new(cls, form):
        # time.time() 是 float 类型
        t = int(time.time())
        form.update(dict(
            created_time=t,
            updated_time=t,
        ))
        todo = super().new(form)
        return todo

    # 只在前端显示时才调用, 这样可以保存原始的 unix time 到数据库中
    def formatted_created_time(self):
        return formatted_time(self.created_time)

    def formatted_updated_time(self):
        return formatted_time(self.updated_time)
