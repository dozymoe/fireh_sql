from .delete_sql import DeleteSQL
from .insert_sql import InsertSQL
from .select_sql import SelectSQL


class SchemaBase(object):

    TABLE_NAME = None

    PRIMARY_KEY_FIELDS = ('id',)

    INSERT_FIELDS = ()
    SELECT_FIELDS = ('id',)
    FILTER_BY_FIELDS = ('id',)
    ORDER_BY_FIELDS = ('id',)

    DELETE_SQL_CLASS = DeleteSQL
    INSERT_SQL_CLASS = InsertSQL
    SELECT_SQL_CLASS = SelectSQL

    PLACEHOLDER = '%s' # used by psycopg2, and '?' for sqlite3


    @classmethod
    def literal_primary_key(cls):
        return ', '.join(cls.PRIMARY_KEY_FIELDS)


    @classmethod
    def create_delete_sql(cls):
        return cls.DELETE_SQL_CLASS(cls)


    @classmethod
    def create_insert_sql(cls):
        return cls.INSERT_SQL_CLASS(cls)


    @classmethod
    def create_select_sql(cls):
        return cls.SELECT_SQL_CLASS(cls)
