from contextlib import contextmanager

import psycopg2
from psycopg2.extras import NamedTupleCursor

DB_USER = 'docker'
DB_PASS = 'docker'
DB_HOST = 'localhost'
DB_PORT = '25432'
DB_NAME = 'gis'

url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


@contextmanager
def Cursor():
    with psycopg2.connect(url) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            yield cursor
            conn.commit()
