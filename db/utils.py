"""
    Callback-based toolkit for sqlite3
"""
import re
import sqlite3
import sys

from config.db_config import DATABASE
from config import BASE_PATH
from typing import Callable
import subprocess
import os
import importlib.util
import logging

logger = logging.getLogger(os.path.dirname(__file__))


class Operation:
    _callbacks: list[Callable] = []
    connection: sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self, connection):
        self.connection = connection
        self._cursor = connection.cursor()

    #def __del__(self):
    #    self.connection.cursor().close()

    def do_commit(self):
        self.connection.commit()

    def run(self):
        for callback in self.callbacks:
            callback()
        return self.cursor.fetchall()

    def clean(self):
        self._callbacks = []

    @property
    def cursor(self):
        if self._cursor:
            return self._cursor
        self._cursor = self.connection.cursor()
        return self._cursor

    @property
    def callbacks(self):
        return self._callbacks


class Migration(Operation):
    connection: sqlite3.Connection
    name: str

    def make_migrations_table(self):
        cursor = self.connection.cursor()
        sql = """
            CREATE TABLE Migrations (
                id INTEGER PRIMARY KEY,
                migration_name VARCHAR(100)
            )
        """
        cursor.execute(sql)
        self.do_commit()

    def apply_migration(self):
        cursor: sqlite3.Cursor
        cursor = self.cursor
        sql = """
                INSERT INTO Migrations VALUES (
                    ?, ?
                )
        """
        row = [None, self.name]
        cursor.execute(sql, row)

    def run(self):
        cursor = self.cursor
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if ('Migrations',) not in tables:
            self.make_migrations_table()
        name = self.name
        sql = """
                    SELECT id FROM Migrations
                    WHERE migration_name = ?
        """
        cursor.execute(sql, [name])
        result = cursor.fetchone()
        if result is None:
            self.apply_migration()
        super().run()
        self.do_commit()

    @staticmethod
    def detect_property(on_inspect):
        """
        Detects 'create' and 'alter' prefix
        :param on_inspect:
        :return:
        """
        callbacks = []
        properties = sorted(
            list(on_inspect.__dict__.items()),
            key=lambda item: item[0], reverse=True
        )
        # collect creates
        for prop, func in properties:
            if prop.startswith('create'):
                callbacks.append(func)
        # collect alters
        for prop, func in properties:
            if prop.startswith('alter'):
                callbacks.append(func)
        return callbacks

    @property
    def callbacks(self) -> list[Callable]:
        """
            Detects and sets callbacks
            :return:
        """

        return self._callbacks


class ConnectionFactory:
    _db = None

    def __init__(self, database=DATABASE):
        self._db = sqlite3.connect(BASE_PATH/database['name'])

    @property
    def db(self):
        return self._db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


class MigrationExecutor:
    def __init__(self):
        self.migrations_py = []
        migrations_py = os.listdir(BASE_PATH/'db/migrations')
        mig_mask = re.compile(r'__\d{3}__\w+__.py')
        for i in migrations_py:
            if re.search(mig_mask, i):
                self.migrations_py.append(i)

    def run(self):
        #for i in self.migrations_py:
        #    logger.debug(subprocess.run(['python', BASE_PATH/'db/migrations'/i]))
        for i in self.migrations_py:
            spec = importlib.util.spec_from_file_location(i[:-3], BASE_PATH/'db/migrations'/i)
            migration = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(migration)
            if migration:
                migration.run()


class QueryExecutor(Operation):

    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)

    def add_query(self, query_callback):
        """
        Appends QueryExecutor with a new callback
        :param query_callback: query function
        :return: None
        """
        def wrapper():
            """
                We have to wrap execution to provide function-execution in self.run()
                :return: None
            """
            query_args = query_callback()
            cursor = self.cursor
            cursor.execute(*query_args)

        self._callbacks.append(
            lambda: wrapper()
        )

    def run(self):
        """
        Executes all queries and cleans callbacks
        :return:
        """
        result = super(QueryExecutor, self).run()
        self.clean()
        return result


def query(func):
    def query_wrapper(*args, **kwargs):
        return lambda: func(*args, **kwargs)
    return query_wrapper
