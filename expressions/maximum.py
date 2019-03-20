from .expression import Expression

class Maximum(Expression):

    def __str__(self):
        expr = 'MAX(%s)' % self.field.id

        if self.alias:
            expr += ' AS ' + self.alias

        return expr
