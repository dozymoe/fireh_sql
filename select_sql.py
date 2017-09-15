from .expressions import Expression
from .filter_by import FilterByMixin
from .order_by import OrderByMixin
from .sql import SQL


class SelectSQL(SQL, FilterByMixin, OrderByMixin):

    fields = None
    page_size = None
    page_offset = None

    def __init__(self, schema):
        super().__init__(schema=schema)
        self.fields = []


    def clear_fields(self):
        self.fields = []


    def set_fields(self, *fields):
        for field in fields:
            if isinstance(field, Expression):
                field.validate_as_field(self.schema)
            else:
                self.schema.validate_select_field_name(field)

            self.fields.append(field)


    def set_limit(self, size, offset=None):
        if size is None:
            self.page_size = None
        else:
            self.page_size = int(size)

        if offset is not None:
            self.page_offset = int(offset)


    def get_data(self):
        for field in self.fields:
            if isinstance(field, Expression):
                for data in field.get_data():
                    yield data

        for filter_ in self.filters:
            for data in filter_.data:
                yield data


    def __str__(self):
        if self.fields:
            fields = ', '.join(str(f) for f in self.fields)
        else:
            fields = '*'

        sql = [
            'SELECT ' + fields,
            'FROM ' + self.schema.TABLE_NAME,
        ]

        expression = ' AND '.join(str(filter_) for filter_ in self.filters)
        if expression:
            sql.append('WHERE ' + expression)

        expression = ', '.join(self.order_fields)
        if expression:
            sql.append('ORDER BY ' + expression)

        if self.page_size and self.page_size > 0:
            sql.append('LIMIT %i OFFSET %i' % (self.page_size,
                    self.page_offset))

        return ' '.join(sql)
