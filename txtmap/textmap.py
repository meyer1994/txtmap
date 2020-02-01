from collections import namedtuple

from txtmap.database import Cursor

Item = namedtuple('Item', ['x', 'y', 'char'])


class TextMap(object):
    def __init__(self):
        super(TextMap, self).__init__()

    def get(self, x, y):
        sql = r'''
        SELECT x, y, char FROM item WHERE Point(x, y) ~= Point(%s, %s)
        '''
        values = (x, y)

        with Cursor() as cursor:
            cursor.execute(sql, values)
            result = cursor.fetchone()

        # Filter values not set
        if result is None:
            return Item(x, y, ' ')
        return Item(*result)

    def set(self, x, y, char):
        sql = r'''
        INSERT INTO item (x, y, char)
        VALUES (%s, %s, %s)
        ON CONFLICT (x, y)
        DO
            UPDATE SET char = EXCLUDED.char
        '''
        values = (x, y, char)
        with Cursor() as cursor:
            cursor.execute(sql, values)

    def area(self, x, y, width, height):
        # Creates empty area
        area = {}
        for i in range(x, x + width):
            for j in range(y, y + height):
                area[(i, j)] = ' '

        sql = r'''
        SELECT x, y, char FROM item
        WHERE Box(Point(%s, %s), Point(%s, %s)) @> Point(x, y)
        '''
        values = (x, y, x + width - 1, y + height - 1)
        with Cursor() as cursor:
            cursor.execute(sql, values)

            # Fill returned values
            for item in cursor.fetchall():
                area[(item.x, item.y)] = item.char

        # Return list of items
        return [Item(x, y, c) for (x, y), c in area.items()]
