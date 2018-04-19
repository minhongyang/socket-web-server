from models import Model
from models.Comment import Comment


class Weibo(Model):
    user_id: int
    content: str

    def comments(self):
        return Comment.find_all(weibo_id=self.id)

    def delete_comments(self):
        comments = self.comments()
        for c in comments:
            Comment.delete(id=c.id)
