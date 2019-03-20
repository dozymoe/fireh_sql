from .expression import Expression

class Sum(Expression):

    def __str__(self):
        expr = 'SUM(%s)' % self.field.id

        if self.alias:
            expr += ' AS ' + self.alias

        return expr
