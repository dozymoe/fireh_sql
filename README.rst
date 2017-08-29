FirehSQL
========

* License   : GPL v3


Summary
-------

This project is meant to be used for psycopg2.

Example:


.. code:: python

    from fireh_sql import SchemaBase

    class UserSchema(SchemaBase):

        TABLE_NAME = 'users'

        FILTER_BY_FIELDS = ('id', 'username', 'email')
        ORDER_BY_FIELDS = ('username',)

        INSERT_FIELDS = ('username', 'email', 'password', 'modified_at',
                'is_superuser', 'is_staff')

        SELECT_FIELDS = ('id', 'username', 'email')
        UPDATE_FIELDS = ('is_superuser', 'is_staff', 'modified_at')


.. code:: python

    import psycopg2

    from .schema import UserSchema

    def insert():
        sql = UserSchema.create_insert_sql()
        sql.set_values(
                username='User1',
                password='User1Password',
                email='User1@example.com')

        with psycopg2.connect('dbname=testdb') as conn:
            with conn.cursor() as cur:
                cur.execute(str(sql), sql.data)
                
            conn.commit()


    def select():
        sql = UserSchema.create_select_sql()

        filter_ = sql.create_or_filter()
        filter_.add(('username', 'Ach%', 'LIKE'))
        filter_.add(('username', 'Abd%', 'LIKE'))
        sql.set_filters(filter_)

        for sort_field in ('username', '-id'):
            sql.add_order_by(sort_field)

        page_size = 10
        page = 1
        page_offset = (page - 1) * page_size
        sql.set_limit(page_size, page_offset)

        with psycopg2.connect('dbname=testdb') as conn:
            with conn.cursor() as cur:
                cur.execute(str(sql), sql.data)


    def update():
        sql = UserSchema.create_update_sql()

        sql.set_values(
                is_superuser=True,
                is_staff=True)

        sql.set_filters(
                ('username', 'User1', '='))

        with psycopg2.connect('dbname=testdb') as conn:
            with conn.cursor() as cur:
                cur.execute(str(sql), sql.data)
