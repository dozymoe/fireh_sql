class OrderByMixin(object):

    order_fields = None

    def __init__(self):
        super().__init__()
        self.order_fields = []


    def add_order_by(self, expression):
        is_desc = expression.startswith('-')
        if is_desc:
            field = expression[1:]
        else:
            field = expression

        if (self.schema.ORDER_BY_FIELDS and\
                field in self.schema.ORDER_BY_FIELDS) or\
                (not self.schema.ORDER_BY_FIELDS and\
                field in self.schema.FIELDS):

            if is_desc:
                self.order_fields.append(field + ' DESC')
            else:
                self.order_fields.append(field)
        else:
            raise RuntimeError('Invalid field: %s for table: %s.' % (
                    field, self.schema.TABLE_NAME))
