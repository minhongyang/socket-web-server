import hashlib
from models import Model


class User(Model):
    password: str

    @staticmethod
    def hashed_password(password, salt='!@#$%^'):
        salted = password + salt
        hashed = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hashed

    def valid_register(self):
        user = User.find_by(username=self.username)
        if user is None:
            self.password = self.hashed_password(self.password)
            return True
        else:
            return False

    def valid_login(self):
        user = User.find_by(username=self.username)
        if user is not None:
            return user.password == self.hashed_password(self.password)
        else:
            return False
