class Expression(object):

    schema = None

    def validate_as_field(self, schema):
        schema.validate_field_name(str(self.field))
        self.schema = schema


    def validate_as_filter(self, schema):
        self.validate_as_field(schema)


    def get_data(self):
        return []


    def __str__(self):
        return ''
