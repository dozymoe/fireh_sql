from .filter_by import FilterByMixin
from .sql import SQL


class DeleteSQL(SQL, FilterByMixin):

    def get_data(self):
        for filter_ in self.filters:
            for data in filter_.data:
                yield data


    def __str__(self):
        sql = [
            'DELETE FROM ' + self.schema.TABLE_NAME,
        ]

        if self.filters:
            sql.append('WHERE ' + ' AND '.join(str(filter_)\
                    for filter_ in self.filters))

        return ' '.join(sql)
