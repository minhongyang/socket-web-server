import time

from models import Model


class Cookie(Model):
    user_id: int
    session_id: str

    def __init__(self, form):
        super().__init__(form)
        self.expired_time = time.time() + 3600
