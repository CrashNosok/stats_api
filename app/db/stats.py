import sqlalchemy

from .base import metadata
from core.config import decimal_max_digits, decimal_places


Stats = sqlalchemy.Table(
    'stats',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('date', sqlalchemy.Date),
    sqlalchemy.Column('views', sqlalchemy.Integer),
    sqlalchemy.Column('clicks', sqlalchemy.Integer),
    sqlalchemy.Column('cost', sqlalchemy.DECIMAL(precision=decimal_max_digits, scale=decimal_places)),
)
