from .expression import Expression

class Minimum(Expression):

    def __str__(self):
        expr = 'MIN(%s)' % self.field.id

        if self.alias:
            expr += ' AS ' + self.alias

        return expr
