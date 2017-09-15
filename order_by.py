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

        self.schema.validate_order_field_name(field)
        if is_desc:
            self.order_fields.append(field + ' DESC')
        else:
            self.order_fields.append(field)


    def clear_order_by(self):
        self.order_fields = []
