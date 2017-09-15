from .expressions import Expression
from .sql import SQL


class InsertSQL(SQL):

    fields = None

    def __init__(self, schema):
        super().__init__(schema=schema)
        self.fields = {}


    def set_values(self, **kwargs):
        for key, value in kwargs.items():
            self.schema.validate_insert_field_name(key)
            if isinstance(value, Expression):
                self.schema.validate_as_field(value)

            self.fields[key] = value


    def get_data(self):
        for value in self.fields.values():
            if isinstance(value, Expression):
                for expr_data in value.get_data():
                    yield expr_data
            else:
                yield value


    def __str__(self):
        sql = [
            'INSERT INTO ' + self.schema.TABLE_NAME,
            '(%s)' % ', '.join(self.fields.keys()),
        ]

        values = []
        for value in self.fields.values():
            if isinstance(value, Expression):
                values.append(str(value))
            else:
                values.append(self.schema.PLACEHOLDER)
        sql.append('VALUES (%s)' % ', '.join(values))

        if self.schema.RETURNING_FIELDS:
            sql.append('RETURNING ' + ', '.join(self.schema.RETURNING_FIELDS))

        return ' '.join(sql)
