import os
from pathlib import Path
from typing import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.orm.session import close_all_sessions

from api.api import api
from app import assign_router
from database import get_db
from infra.table.url_table import table_registry
from setting import settings

DB_URL = f'sqlite:///./{settings.db_dir}/test_url_service.db?check_same_thread=False'


@pytest.fixture(scope='module')
def test_client() -> TestClient:
    client = TestClient(api)
    assign_router()
    yield client


class TestingSession(Session):
    def commit(self):
        self.flush()
        self.expire_all()


@pytest.fixture(scope='function', autouse=True)
def test_db() -> Generator:
    root_path = Path(__file__).parent.parent
    if not os.path.exists(f'{root_path}/{settings.db_dir}'):
        os.mkdir(f'{root_path}/{settings.db_dir}')

    engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
    Base = table_registry.generate_base()
    Base.metadata.create_all(bind=engine)

    function_scope = uuid4().hex
    TestSessionLocal = scoped_session(
        sessionmaker(class_=TestingSession, autocommit=False, autoflush=False, bind=engine),
        scopefunc=lambda: function_scope,
    )
    Base.query = TestSessionLocal.query_property()

    db = TestSessionLocal()

    def get_db_for_testing():
        try:
            yield db
            db.commit()
        except SQLAlchemyError as e:
            assert e is not None
            db.rollback()

    api.dependency_overrides[get_db] = get_db_for_testing

    yield db

    # Remove test records
    db.rollback()
    close_all_sessions()
    engine.dispose()
