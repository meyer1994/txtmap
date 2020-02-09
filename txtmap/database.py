from collections import namedtuple, defaultdict
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import NamedTupleCursor

Item = namedtuple('Item', ['x', 'y', 'char'])


@contextmanager
def Cursor(url):
    try:
        conn = psycopg2.connect(url)
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                yield cursor
                conn.commit()
    finally:
        conn.close()


class TextMap(object):
    def __init__(self, url):
        super(TextMap, self).__init__()
        self.url = url

    def get(self, x, y):
        sql = r'SELECT x, y, char FROM item WHERE Point(x, y) ~= Point(%s, %s)'
        values = (x, y)

        with Cursor(self.url) as cursor:
            cursor.execute(sql, values)
            result = cursor.fetchone()

        if result is None:
            return Item(x, y, ' ')
        return Item(*result)

    def set(self, x, y, char):
        sql = r'''
        INSERT INTO item (x, y, char) VALUES (%s, %s, %s)
        ON CONFLICT (x, y) DO
            UPDATE SET char = EXCLUDED.char
        '''
        values = (x, y, char)

        with Cursor(self.url) as cursor:
            cursor.execute(sql, values)
        return Item(x, y, char)

    def area(self, x, y, width, height):
        # Empty area
        area = {}
        for _x in range(x, x + width):
            for _y in range(y, y + height):
                area[(_x, _y)] = ' '

        sql = r'''
        SELECT x, y, char FROM item
            WHERE Box(Point(%s, %s), Point(%s, %s)) @> Point(x, y)
        '''
        values = (x, y, x + width - 1, y + height - 1)

        with Cursor(self.url) as cursor:
            cursor.execute(sql, values)
            result = cursor.fetchall()

        # Fill values
        for item in result:
            area[(item.x, item.y)] = item.char

        # Return list of items
        return [Item(x, y, c) for (x, y), c in area.items()]


class Connections(object):
    def __init__(self, url):
        super(Connections, self).__init__()
        self.url = url

    def add(self, _id):
        sql = r'''INSERT INTO connection (id) VALUES (%s)'''
        values = (_id, )
        with Cursor(self.url) as cursor:
            cursor.execute(sql, values)
        return _id

    def remove(self, _id):
        sql = r'''DELETE FROM connection WHERE id = %s'''
        values = (_id, )
        with Cursor(self.url) as cursor:
            cursor.execute(sql, values)
        return _id

    def all(self):
        sql = r'''SELECT id FROM connection'''
        with Cursor(self.url) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        return [r.id for r in results]
