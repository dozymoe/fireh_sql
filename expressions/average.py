from .expression import Expression

class Average(Expression):

    def __str__(self):
        expr = 'AVG(%s)' % self.field.id

        if self.alias:
            expr += ' AS ' + self.alias

        return expr
