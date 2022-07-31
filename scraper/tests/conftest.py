import pytest
from peewee import SqliteDatabase

from app.db import Product, Schedule

MODELS = (Product, Schedule)


@pytest.fixture
def test_db():
    connection = SqliteDatabase(':memory:')
    for model in MODELS:
        model._meta.database = connection
    connection.create_tables(MODELS)
    connection.commit()
    yield connection
    connection.close()
