from .expression import Expression

class Count(Expression):

    field = None
    alias = None
    schema = None

    def __init__(self, field, alias=None):
        self.field = field or ''
        self.alias = alias


    def validate_as_field(self, schema):
        if self.field and self.field != '*':
            schema.validate_field_name(str(self.field))
        self.schema = schema


    def __str__(self):
        expr = 'COUNT(%s)' % str(self.field)

        if self.alias:
            expr += ' AS ' + self.alias

        return expr
