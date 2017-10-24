from ..expressions import Expression
from ..update_sql import UpdateSQL

class OnConflictUpdate(UpdateSQL):

    def __str__(self):
        sql = ['DO UPDATE']

        expressions = []
        for key, value in self.fields.items():
            if isinstance(value, Expression):
                expressions.append('%s=%s' % (key, str(value)))
            else:
                expressions.append('%s=%s' % (key, self.schema.PLACEHOLDER))
        if expressions:
            sql.append('SET ' + ', '.join(expressions))

        expression = ' AND '.join(str(filter_) for filter_ in self.filters)
        if expression:
            sql.append('WHERE ' + expression)

        return ' '.join(sql)
