from .expressions import Expression
from .filter_by import FilterByMixin
from .sql import SQL


class UpdateSQL(SQL, FilterByMixin):

    fields = None

    def __init__(self, schema):
        super().__init__(schema=schema)
        self.fields = {}


    def set_values(self, **kwargs):
        for key, value in kwargs.items():
            self.schema.validate_update_field_name(key)
            if isinstance(value, Expression):
                value.validate_as_field(self.schema)

            self.fields[key] = value


    def get_data(self):
        for value in self.fields.values():
            if isinstance(value, Expression):
                for data in value.get_data():
                    yield data
            else:
                yield value

        for filter_ in self.filters:
            for data in filter_.data:
                yield data


    def __str__(self):
        sql = [
            'UPDATE ' + self.schema.TABLE_NAME,
        ]

        expressions = []
        for key, value in self.fields:
            if isinstance(value, Expression):
                expressions.append('%s=%s' % (key, str(value)))
            else:
                expressions.append('%s=%s' % (key, self.schema.PLACEHOLDER))
        if expressions:
            sql.append('SET ' + ', '.join(expressions))

        expression = ' AND '.join(str(filter_) for filter_ in self.filters)
        if expression:
            sql.append('WHERE ' + expression)

        return ' '.join(sql)
