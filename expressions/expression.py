class Expression(object):

    def validate_as_field(self, schema):
        pass


    def validate_as_filter(self, schema):
        self.validate_as_field(schema)


    def get_data(self):
        return []


    def __str__(self):
        return ''
