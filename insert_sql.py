from .sql import SQL


class InsertSQL(SQL):

    fields = None

    def __init__(self, schema):
        super().__init__(schema=schema)
        self.fields = {}


    def set_values(self, **kwargs):
        for key, value in kwargs.items():
            if (self.schema.INSERT_FIELDS and\
                    key in self.schema.INSERT_FIELDS) or\
                    (not self.schema.INSERT_FIELDS and\
                    key in self.schema.FIELDS):

                self.fields[key] = value
            else:
                raise RuntimeError('Invalid field: %s for table: %s.' % (
                        key, self.schema.TABLE_NAME))


    def get_data(self):
        for data in self.fields.values():
            yield data


    def __str__(self):
        sql = [
            'INSERT INTO ' + self.schema.TABLE_NAME,
            '(%s)' % ', '.join(self.fields.keys()),
            'VALUES (%s)' % ', '.join([self.schema.PLACEHOLDER] *\
                    len(self.fields)),
        ]

        if self.schema.RETURNING_FIELDS:
            sql.append('RETURNING ' + ', '.join(self.schema.RETURNING_FIELDS))

        return ' '.join(sql)
