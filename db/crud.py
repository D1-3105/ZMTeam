import sqlite3
from .utils import query


class TableCreation:
    connection: sqlite3.Connection

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create_profile_table(self):
        """
            ID - fqdn of a site
            dt_creation - date time of creation
            cookie_val - json dumped cookies obtained from this site
            dt_execution - datetime of last execution
            exec_num - number of executions
        """
        cursor = self.connection.cursor()
        sql = """
            CREATE TABLE Cookie_Profile (
            id TEXT PRIMARY KEY,
            dt_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
            cookie_val TEXT NULL,
            dt_execution DATETIME NULL,
            exec_num INT DEFAULT 0
        )
        """
        cursor.execute(sql)
        # no commit, because all the operations should be wrapped in one commit


@query
def update_profile_query(**update_kwargs):
    """
    :param update_kwargs:
    :return: kwargs for cursor
    """
    if 'id' not in update_kwargs:
        raise ValueError("Missing 'id' parameter in update_kwargs")
    profile_id = update_kwargs.pop('id')
    set_clause = ', '.join(["{} = ?".format(k) for k in update_kwargs.keys()])
    sql = """
        UPDATE Cookie_Profile 
        SET {} 
        WHERE id = ?
    """.format(set_clause)
    query_params = [v for v in update_kwargs.values()]
    query_params.append(profile_id)
    return sql, query_params


@query
def exists_profile_query(profile_id: str):
    """
        :param profile_id: fqdn of a site
        :return: kwargs for cursor
    """
    sql = f"""
        SELECT EXISTS(
            SELECT id FROM Cookie_Profile 
            WHERE id = ?
        )
    """
    return sql, [profile_id]


@query
def create_profile_query(**create_kwargs):
    """
    :param create_kwargs: {field:value}
    :return: kwargs for cursor
    """
    insert_clause = ', '.join(create_kwargs.keys())
    values_clause = ', '.join(['?'] * len(create_kwargs.keys()))
    sql = f'''
        INSERT INTO Cookie_Profile ({insert_clause})
        VALUES 
        ({values_clause})
    '''
    query_params = []
    query_params.extend(create_kwargs.values())
    return sql, query_params


@query
def select_profile_query(profile_id: str, *fields):
    """
        :param profile_id: fqdn of a site
        :return:
    """
    fields_clause = ', '.join(fields)
    sql = """
        SELECT {} FROM Cookie_Profile 
        WHERE id = ?
    """.format(fields_clause)
    return sql, [profile_id]
