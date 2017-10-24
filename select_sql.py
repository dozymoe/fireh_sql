from .expressions import Expression
from .filter_by import FilterByMixin
from .order_by import OrderByMixin
from .sql import SQL


class SelectSQL(SQL, FilterByMixin, OrderByMixin):

    fields = None
    page_size = None
    page_offset = None
    groupby_exprs = None
    having_exprs = None

    def __init__(self, schema):
        super().__init__(schema=schema)
        self.fields = []
        self.groupby_exprs = []
        self.having_exprs = []


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


    def set_group_by(self, *expressions):
        for expression in expressions:
            if isinstance(expression, str):
                self.schema.validate_field_name(expression)
            elif isinstance(expression, Expression):
                expression.validate_as_field(self.schema)
            else:
                raise RuntimeError('SelectSQL.set_group_by ' +\
                        'only supports field name or expression.')

            self.groupby_exprs.append(expression)


    def set_having(self, *expressions):
        for expression in expressions:
            if isinstance(expression, Expression):
                expression.validate_as_field(self.schema)
            else:
                raise RuntimeError('SelectSQL.set_having ' +\
                        'only supports expression.')

            self.having_exprs.append(expression)


    def get_data(self):
        for field in self.fields:
            if isinstance(field, Expression):
                for data in field.data:
                    yield data

        for filter_ in self.filters:
            for data in filter_.data:
                yield data

        for expression in self.groupby_exprs:
            if isinstance(expression, Expression):
                for data in expression.data:
                    yield data

        for expression in self.having_exprs:
            if isinstance(expression, Expression):
                for data in expression.data:
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

        if self.groupby_exprs:
            sql.append('GROUP BY ' + ', '.join(str(expr) \
                    for expr in self.groupby_exprs))

        if self.having_exprs:
            sql.append('HAVING ' + ', '.join(str(expr) \
                    for expr in self.having_exprs))

        expression = ', '.join(self.order_fields)
        if expression:
            sql.append('ORDER BY ' + expression)

        if self.page_size and self.page_size > 0:
            sql.append('LIMIT %i OFFSET %i' % (self.page_size,
                    self.page_offset))

        return ' '.join(sql)
