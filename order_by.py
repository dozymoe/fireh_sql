class OrderByMixin(object):

    order_fields = None

    def __init__(self):
        super().__init__()
        self.order_fields = []


    def set_sorting_order(self, *expressions):
        for expression in expressions:
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


    def find_sorting_order(self, data, fields):
        if data is None:
            return

        db_fields = []
        form_fields = []
        for field in fields:
            if isinstance(field, (list, tuple)):
                db_fields.append(field[0])
                form_fields.append(field[1])
            else:
                db_fields.append(field)
                form_fields.append(field)

        for expression in data:
            is_desc = expression.startswith('-')
            if is_desc:
                field = expression[1:]
            else:
                field = expression

            try:
                idx = form_fields.index(field)
                if form_fields[idx] == db_fields[idx]:
                    yield expression
                elif is_desc:
                    yield '-' + db_fields[idx]
                else:
                    yield db_fields[idx]
            except ValueError:
                pass
