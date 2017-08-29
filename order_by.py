class OrderByMixin(object):

    order_fields = None

    def __init__(self):
        super().__init__()
        self.order_fields = []


    def add_order_by(self, expression):
        if expression.startswith('-'):
            self.order_fields.append(expression[1:] + ' DESC')
        else:
            self.order_fields.append(expression)
