import pytest
from .fixtures import db
from db.utils import QueryExecutor
from db.crud import create_profile_query, select_profile_query, update_profile_query
from datetime import datetime


def test_profile_creation(db):
    create = create_profile_query(
        id='google.com',
        #dt_creation=datetime.now(),
        cookie_val='12345',
        #dt_execution=None,
        exec_num=0
    )
    executor = QueryExecutor(db)
    executor.add_query(create)
    executor.run()
    executor.do_commit()
    select = select_profile_query('google.com', 'id', 'cookie_val')
    executor.add_query(select)
    result = executor.run()
    print('RESULT', result)
    assert len(result) != 0


def test_profile_update(db):
    create = create_profile_query(
        id='google.com',
        # dt_creation=datetime.now(),
        cookie_val='12345',
        # dt_execution=None,
        exec_num=0
    )
    executor = QueryExecutor(db)
    executor.add_query(create)
    update = update_profile_query(
        id='google.com',
        cookie_val='123456'
    )
    executor.add_query(update)
    executor.run()
    executor.do_commit()
    select = select_profile_query('google.com', 'id', 'cookie_val')
    executor.add_query(select)
    result = executor.run()
    print(result)
    assert result is not []


