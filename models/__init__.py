import json

from utils import log


class Model(object):
    id: int
    username: str

    def __init__(self, form):
        annotations = {}
        annotations.update(self.__annotations__)
        annotations.update(Model.__annotations__)
        for name, var_type in annotations.items():
            if name in form:
                value = form[name]
                value = var_type(value)
                setattr(self, name, value)
            else:
                setattr(self, name, var_type())

    # 利用 annotations 简化之前，比较传统的方法，问题也不大
    # def __init__(self, form):
    #     self.id = form.get('id', 0)

    @classmethod
    def load_file(cls):
        path = cls.data_path()
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
        return json.loads(data)

    @classmethod
    def save_file(cls, data):
        path = cls.data_path()
        data = json.dumps(data, indent=2, ensure_ascii=False)
        with open(path, 'w+', encoding='utf-8') as file:
            file.write(data)

    @classmethod
    def data_path(cls):
        path = 'data/{}.txt'.format(cls.__name__)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def all(cls):
        data = cls.load_file()
        models = [cls(d) for d in data]
        return models

    def save(self):
        models = self.all()
        first_index = 1
        if self.id == 0:
            if len(models) == 0:
                self.id = first_index
            else:
                self.id = models[-1].id + 1
            models.append(self)
        else:
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        ld = [m.__dict__ for m in models]
        self.save_file(ld)

    @classmethod
    def find_by(cls, **kwargs):
        for model in cls.all():
            match = True
            for k, v in kwargs.items():
                if getattr(model, k) != v:
                    match = False
            if match:
                return model
        return None

    @classmethod
    def find_all(cls, **kwargs):
        models = []
        for m in cls.all():
            match = True
            for k, v in kwargs.items():
                if getattr(m, k) != v:
                    match = False
            if match:
                models.append(m)
        return models

    @classmethod
    def delete(cls, **kwargs):
        models = []
        for model in cls.all():
            match = True
            for k, v in kwargs.items():
                if getattr(model, k) != v:
                    match = False
            if match is False:
                models.append(model)

        ld = [m.__dict__ for m in models]
        cls.save_file(ld)

    @classmethod
    def update(cls, id, form):
        model = cls.find_by(id=id)
        for k, v in form.items():
            if k in cls.__annotations__:
                setattr(model, k, v)
        model.save()
