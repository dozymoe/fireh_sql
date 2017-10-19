from .expression import Expression

class Minimum(Expression):

    field = None
    alias = None

    def __init__(self, field, alias=None):
        self.field = field
        self.alias = alias


    def validate_as_field(self, schema):
        schema.validate_field_name(str(self.field))
        self.schema = schema


    def __str__(self):
        expr = 'MIN(%s)' % str(self.field)

        if self.alias:
            expr += ' AS ' + self.alias

        return expr
