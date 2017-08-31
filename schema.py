from .delete_sql import DeleteSQL
from .insert_sql import InsertSQL
from .select_sql import SelectSQL
from .update_sql import UpdateSQL


class SchemaBase(object):

    TABLE_NAME = None

    FIELDS = ('id',)

    PRIMARY_KEY_FIELDS = ('id',)

    INSERT_FIELDS = () # Whitelist fields of Insert Query
    SELECT_FIELDS = () # Whitelist fields returned by Select Query
    UPDATE_FIELDS = () # Whitelist fields of Update Query

    FILTER_BY_FIELDS = () # Whitelist fields can be used in WHERE clause
    ORDER_BY_FIELDS = () # Whitelist fields can be used in ORDER BY clause

    DELETE_SQL_CLASS = DeleteSQL
    INSERT_SQL_CLASS = InsertSQL
    SELECT_SQL_CLASS = SelectSQL
    UPDATE_SQL_CLASS = UpdateSQL

    PLACEHOLDER = '%s' # used by psycopg2, and '?' for sqlite3
    RETURNING_FIELDS = () # fields in postgresql RETURNING clause


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


    @classmethod
    def create_update_sql(cls):
        return cls.UPDATE_SQL_CLASS(cls)
