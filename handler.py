import os

from txtmap.handler import Handler

DB_URL = os.environ['DB_URL']

handler = Handler(DB_URL)
