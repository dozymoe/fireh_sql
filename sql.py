class SQL(object):

    schema = None

    def __init__(self, schema):
        super().__init__()
        self.schema = schema


    @property
    def data(self):
        return tuple(self.get_data())


    def get_data(self):
        raise NotImplementedError()
