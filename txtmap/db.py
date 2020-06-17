import orm
import databases
import sqlalchemy

from txtmap.config import config

database = databases.Database(config.DATABASE_URL)
metdata = sqlalchemy.MetaData()


class Coordinate(orm.Model):
    __tablename__ = 'coordinates'
    __database__ = database
    __metadata__ = metdata

    x = orm.Integer(primary_key=True)
    y = orm.Integer(primary_key=True)
    c = orm.String(min_length=1, max_length=1, trim_whitespace=False)


engine = sqlalchemy.create_engine(config.DATABASE_URL)
metdata.create_all(engine)
