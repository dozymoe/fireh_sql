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
        self.page_size = 20
        self.page_offset = 0


    def set_fields(self, *fields):
        for field in fields:
            if (self.schema.SELECT_FIELDS and\
                    field in self.schema.SELECT_FIELDS) or\
                    (not self.schema.SELECT_FIELDS and\
                    field in self.schema.FIELDS):

                self.fields.append(field)
            else:
                raise RuntimeError('Invalid field: %s for table: %s.' % (
                        field, self.schema.TABLE_NAME))


    def set_limit(self, size=None, offset=None):
        if size is not None:
            self.page_size = int(size)

        if offset is not None:
            self.page_offset = int(offset)


    def get_data(self):
        for filter_ in self.filters:
            for data in filter_.data:
                yield data


    def __str__(self):
        if self.fields:
            fields = ', '.join(self.fields)
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

        sql.append('LIMIT %i OFFSET %i' % (self.page_size, self.page_offset))

        return ' '.join(sql)
