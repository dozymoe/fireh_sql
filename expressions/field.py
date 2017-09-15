class Field(object):

    name = None
    alias = None

    def __init__(self, name, alias=None):
        self.name = name
        self.alias = alias


    def validate_as_field(self, schema):
        schema.validate_field_name(self.name)


    def validate_as_filter_by(self, schema):
        schema.validate_filter_field_name(self.name)


    def validate_as_order_by(self, schema):
        schema.valdiate_order_field_name(self.name)
