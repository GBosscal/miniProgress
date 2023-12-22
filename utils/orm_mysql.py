"""
@Project: BackendForPain
@File: orm_mysql.py
@Auth: Bosscal
@Date: 2023/9/4
@Description:
    通过ORM的形式，操作mysql数据库。
"""
import traceback
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from config import Config
from contextlib import contextmanager


def _create_db_session():
    engine = create_engine(Config.get_mysql_url(), echo=Config.MysqlEcho, pool_pre_ping=True)
    session = scoped_session(sessionmaker(bind=engine))
    return session()


@contextmanager
def create_db_session():
    session = _create_db_session()
    try:
        yield session
    except Exception as e:
        print(traceback.format_exc())
        session.rollback()
    finally:
        session.close()
