class Manager(object):
    def __init__(self, model_class, client):
        super().__init__()
        self.model_class = model_class
        model_class._meta.manager = self
        self.client = client