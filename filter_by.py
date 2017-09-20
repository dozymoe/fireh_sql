import logging

from dateutil.parser import parse as dateparse

from .expressions import Expression


class SQLFilter(object):

    schema = None
    fields = None
    separator = ' AND '

    def __init__(self, schema):
        self.schema = schema
        self.fields = []


    def add(self, field_tuple):
        if isinstance(field_tuple, SQLFilter):
            self.fields.append(field_tuple)

        elif isinstance(field_tuple, (list, tuple)):
            self.schema.validate_filter_field_name(field_tuple[0])
            if isinstance(field_tuple[1], Expression):
                field_tuple[1].validate_as_filter(self.schema)

            self.fields.append(field_tuple)

        else:
            raise TypeError('Expecting SQLFilter, list, or tuple.')


    @property
    def data(self):
        for field_tuple in self.fields:
            if isinstance(field_tuple, SQLFilter):
                for data in field_tuple.data:
                    yield data
            elif field_tuple[1] is None:
                pass
            elif isinstance(field_tuple[1], Expression):
                for data in field_tuple[1].get_data():
                    yield data
            elif isinstance(field_tuple[1], (list, tuple)):
                for data in field_tuple[1]:
                    yield data
            else:
                yield field_tuple[1]


    def __str__(self):
        filters = []
        for field_tuple in self.fields:
            if isinstance(field_tuple, SQLFilter):
                filter_expression = str(field_tuple)
                if filter_expression:
                    filters.append('(%s)' % filter_expression)
                continue

            expressions = [field_tuple[0]]
            if len(field_tuple) == 3:
                expressions.append(field_tuple[2])

            if field_tuple[1] is None:
                expressions.append('NULL')

            elif isinstance(field_tuple[1], Expression):
                expressions.append(str(field_tuple[1]))

            elif isinstance(field_tuple[1], (list, tuple)):
                if not field_tuple[1]:
                    continue

                expressions.append(', '.join([self.schema.PLACEHOLDER] *\
                        len(field_tuple[1])))

            else:
                expressions.append(self.schema.PLACEHOLDER)

            filters.append(' '.join(expressions))

        return self.separator.join(filters)


class AndSQLFilter(SQLFilter): pass # pylint:disable=multiple-statements
class OrSQLFilter(SQLFilter):

    separator = ' OR '


class FilterByMixin(object):

    filters = None

    def __init__(self):
        super().__init__()
        self.filters = []


    def create_and_filter(self, *fields):
        filter_ = AndSQLFilter(self.schema)
        for field in fields:
            filter_.add(field)

        return filter_


    def create_or_filter(self, *fields):
        filter_ = OrSQLFilter(self.schema)
        for field in fields:
            filter_.add(field)

        return filter_


    def set_filters(self, *filters):
        flts = []
        for filter_ in filters:
            if isinstance(filter_, SQLFilter):
                self.filters.append(filter_)
            else:
                flts.append(filter_)

        if flts:
            self.filters.append(self.create_and_filter(*flts))


    def find_filters(self, data, fields):
        if data is None:
            return

        for field in fields:
            if isinstance(field, (list, tuple)):
                db_field = field[0]
                form_field = field[1]
            else:
                db_field = form_field = field

            value = data.get(form_field)
            if value is None or len(value) < 2:
                continue

            if value[0] == '=':
                value = value[1:]
                if value == 'null':
                    yield (db_field, None, 'IS')
                else:
                    yield (db_field, value, '=')

            elif value[0] == '!':
                value = value[1:]
                if value == 'null':
                    yield (db_field, None, 'IS NOT')
                else:
                    yield (db_field, value, '<>')

            elif (value[0] == '<' or value[0] == '>')  and value[1] == '=':
                yield (db_field, value[2:], value[:2])

            elif value[0] == '<' or value[0] == '>':
                yield (db_field, value[1:], value[0])

            elif value[0] == '%' or value[-1] == '%':
                yield (db_field, value, 'LIKE')


    def find_datetime_filters(self, data, *fields):
        for filter_ in self.find_filters(data, fields):
            if filter_[1] is None:
                yield filter_
                continue

            try:
                value = dateparse(filter_[1])
                yield (filter_[0], value, filter_[2])
            except (ValueError, OverflowError):
                logging.exception('Invalid Schema filter.')


    def find_numeric_filters(self, data, *fields):
        for filter_ in self.find_filters(data, fields):
            if filter_[1] is None:
                yield filter_
                continue

            try:
                value = int(filter_[1])
                yield (filter_[0], value, filter_[2])
            except (TypeError, ValueError):
                logging.exception('Invalid Schema filter.')
