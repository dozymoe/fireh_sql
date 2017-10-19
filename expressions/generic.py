import re

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
            ),
            total=Generic(
                '{field.0} * {field.1}',
                ['price', count'],
            ),
            price=Generic(
                '{field} - {value} - {value}',
                'price',
                [20, 10],
            ),
        )

    """
    fields = None
    alias = None
    expression = None
    values = None

    def __init__(self, expression, fields=None, values=None, alias=None):
        self.fields = fields
        self.alias = alias
        self.expression = expression
        self.values = values


    def validate_as_field(self, schema):
        if schema.PLACEHOLDER in self.expression:
            raise ValueError('Invalid characters: ' + schema.PLACEHOLDER +\
                    ' in expression: "' + self.expression + '"' +\
                    ' for table: ' + schema.TABLE_NAME + '.')

        if isinstance(self.fields, str):
            schema.validate_field_name(self.fields)

            self.fields = [self.fields]
        elif isinstance(self.fields, (list, tuple)):
            for field in self.fields:
                schema.validate_field_name(field)

        self.expression = re.sub(r'{\s*field\s*}', '{field.0}')

        if isinstance(self.values, str):
            self.values = [self.values]

        self.schema = schema


    def get_data(self):
        if self.values:
            for value in self.values:
                yield value


    def __str__(self):
        replacement = {}

        if self.fields:
            for ii, field in enumerate(self.fields):
                replacement['field.%i' % ii] = field

        if self.values:
            replacement['value'] = self.schema.PLACEHOLDER

        if replacement:
            expr = self.expression % replacement
        else:
            expr = self.expression

        if self.alias:
            expr += ' AS ' + self.alias

        return expr
