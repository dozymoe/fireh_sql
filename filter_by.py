class SQLFilter(object):

    schema = None
    fields = None
    separator = ' AND '

    def __init__(self, schema):
        self.schema = schema
        self.fields = []


    def add(self, field_tuple):
        if len(field_tuple) == 2:
            field_tuple = (field_tuple[0], field_tuple[1], '=')

        if isinstance(field_tuple, SQLFilter):
            self.fields.append(field_tuple)

        elif (self.schema.FILTER_BY_FIELDS and\
                field_tuple[0] in self.schema.FILTER_BY_FIELDS) or\
                (not self.schema.FILTER_BY_FIELDS and\
                field_tuple[0] in self.schema.FIELDS):

            self.fields.append(field_tuple)
        else:
            raise RuntimeError('Invalid field: %s for table: %s.' % (
                    field_tuple[0], self.schema.TABLE_NAME))


    @property
    def data(self):
        for field_tuple in self.fields:
            if isinstance(field_tuple, SQLFilter):
                for data in field_tuple.data:
                    yield data
            elif field_tuple[1] is None:
                pass
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

            elif field_tuple[1] is None:
                filters.append('"%s" %s NULL' % (field_tuple[0],
                        field_tuple[2]))

            elif isinstance(field_tuple[1], (list, tuple)):
                if field_tuple[1]:
                    filters.append('"%s" %s (%s)' % (field_tuple[0],
                        field_tuple[2], ', '.join([self.schema.PLACEHOLDER] *\
                        len(field_tuple[1]))))
            else:
                filters.append('"%s" %s %s' % (field_tuple[0], field_tuple[2],
                        self.schema.PLACEHOLDER))

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
