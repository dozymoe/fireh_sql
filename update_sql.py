from .filter_by import FilterByMixin
from .sql import SQL


class UpdateSQL(SQL, FilterByMixin):

    fields = None

    def __init__(self, schema):
        super().__init__(schema=schema)
        self.fields = {}


    def set_values(self, **kwargs):
        for key, value in kwargs.items():
            if (self.schema.UPDATE_FIELDS and\
                    key in self.schema.UPDATE_FIELDS) or\
                    (not self.schema.UPDATE_FIELDS and\
                    key in self.schema.FIELDS):

                self.fields[key] = value
            else:
                raise RuntimeError('Invalid field: %s for table: %s.' % (
                        key, self.schema.TABLE_NAME))


    def get_data(self):
        for data in self.fields.values():
            yield data
        for filter_ in self.filters:
            for data in filter_.data:
                yield data


    def __str__(self):
        sql = [
            'UPDATE ' + self.schema.TABLE_NAME,
        ]

        expression = ', '.join(key + '=' + self.schema.PLACEHOLDER\
                for key in self.fields)

        if expression:
            sql.append('SET ' + expression)

        expression = ' AND '.join(str(filter_) for filter_ in self.filters)
        if expression:
            sql.append('WHERE ' + expression)

        return ' '.join(sql)
