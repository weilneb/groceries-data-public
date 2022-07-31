from peewee import *
from enum import Enum
from datetime import datetime
import os

import logging

logger = logging.getLogger(__name__)


def get_database():
    db_path = os.getenv('DB_PATH')
    if db_path is None:
        logger.warning('Defaulting to in-memory database.')
        return SqliteDatabase(':memory:')
    else:
        logger.info(f'DB_PATH={db_path}')
        return SqliteDatabase(db_path)


def list_all_products():
    logger.info("Listing products...")
    for p in Product.select():
        logger.info(f"id={p.id_}, url={p.url}, category={p.category}")


def list_all_schedule():
    logger.info("Listing schedule...")
    for s in Schedule.select().order_by(Schedule.id_.desc()).limit(30):
        logger.info(f"{s.id_}, {s.product}, {s.scheduled_for}, {s.status}")


class BaseModel(Model):
    class Meta:
        database = get_database()


class Product(BaseModel):
    id_ = AutoField(column_name='id')
    url = TextField(unique=True)
    category = TextField()

    def __str__(self):
        return self.url


class ScheduleStatus(Enum):
    SCHEDULED = 'scheduled'
    FAILED = 'failed'
    SUCCESS = 'success'

    def __str__(self):
        return self.name


class ScheduleStatusField(TextField):
    field_type = 'schedule_status'

    def db_value(self, value: ScheduleStatus):
        return value.name

    def python_value(self, value: str):
        return ScheduleStatus[value]


class Schedule(BaseModel):
    id_ = AutoField(column_name='id')
    product = ForeignKeyField(Product, backref='product')
    scheduled_for = DateTimeField(default=datetime.now)
    status = ScheduleStatusField(default=ScheduleStatus.SCHEDULED)
    error = TextField(null=True)


def create_tables():
    get_database().create_tables([Product, Schedule])


def get_all_products():
    return list(Product.select())


def get_all_schedules():
    return list(Schedule.select())
