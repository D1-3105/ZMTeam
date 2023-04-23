import sqlite3
from db.utils import Migration, ConnectionFactory
from db.crud import TableCreation


class FirstMigration(Migration):

    connection: sqlite3.Connection
    name = '__001__init__'

    def __init__(self, connection):
        super().__init__(connection)

    def create(self):
        object_creation = TableCreation(self.connection)
        callbacks = self.detect_property(TableCreation)

        def wrap(callback_list):
            for callback in callback_list:
                callback(object_creation)

        return wrap(callbacks)

    def apply_migration(self):
        super(FirstMigration, self).apply_migration()
        self._callbacks = [
            lambda: self.create()
        ]


def run():
    conn = ConnectionFactory().db
    FirstMigration(connection=conn).run()
    conn.close()
