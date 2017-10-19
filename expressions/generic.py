from .expression import Expression

class Generic(Expression):
    """ Create free SQL expression.

    Example:

        sql = Schema.create_update_sql()
        sql.set_values(
            average=Generic(
                '({field} + {value}) / 2', # field and value are reserved words
                'average',                 # table field to change
                123                        # the value; can also be list, tuple
                                           # or None
            )
        )

    """
    field = None
    alias = None
    expression = None
    values = None

    def __init__(self, expression, field, values, alias=None):
        self.field = field or ''
        self.alias = alias
        self.expression = expression
        self.values = values


    def validate_as_field(self, schema):
        if schema.PLACEHOLDER in self.expression:
            raise ValueError('Invalid characters: ' + schema.PLACEHOLDER +\
                    ' in expression: "' + self.expression + '"' +\
                    ' for table: ' + schema.TABLE_NAME + '.')

        if self.field and self.field != '*':
            schema.validate_field_name(str(self.field))

        self.schema = schema


    def get_data(self):
        if self.values is None:
            pass
        elif isinstance(self.values, (list, tuple)):
            for value in self.values:
                yield value
        else:
            yield self.values


    def __str__(self):
        expr = self.expression % {
                'field': self.field,
                'value': self.schema.PLACEHOLDER}

        if self.alias:
            expr += ' AS ' + self.alias

        return expr
