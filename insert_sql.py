from .sql import SQL


class InsertSQL(SQL):

    fields = None

    def __init__(self, schema):
        super().__init__(schema=schema)
        self.fields = {}


    def set_values(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.schema.INSERT_FIELDS:
                self.fields[key] = value
            else:
                raise RuntimeError('Invalid field: %s for table: %s.' % (
                        key, self.schema.TABLE_NAME))


    def get_data(self):
        for data in self.fields.values():
            yield data


    def __str__(self):
        return 'INSERT INTO %s(%s) VALUES(%s) RETURNING %s'  % (
                self.schema.TABLE_NAME,
                ', '.join(self.fields.keys()),
                ', '.join(['%s'] * len(self.fields)),
                self.schema.literal_primary_key())
