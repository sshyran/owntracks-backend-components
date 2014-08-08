#!/usr/bin/env python

from peewee import *
from config import Config
import datetime
import sys

try:
    cf = Config()
except Exception, e:
    print "Can't load configuration: %s" % (str(e))
    sys.exit(1)

pgsql_db = PostgresqlDatabase(cf.get('dbname', 'owntracks'),
    user=cf.get('dbuser'),
    port=cf.get('dbport', 5432),
    threadlocals=True)

class PostgresqlModel(Model):

    class Meta:
        database = pgsql_db

class Location(PostgresqlModel):
    topic           = BlobField(null=False)
    username        = CharField(null=False)
    device          = CharField(null=False)
    lat             = CharField(null=False)
    lon             = CharField(null=False)
    tst             = DateTimeField(default=datetime.datetime.now, index=True)
    acc             = CharField(null=True)
    batt            = CharField(null=True)
    waypoint        = TextField(null=True)  # desc in JSON, but desc is reserved SQL word
    event           = CharField(null=True)
    # optional: full JSON of item including all data from plugins
    json            = TextField(null=True)
    # the following fields must be correlated to settings.py (plugin columns)
    weather         = CharField(null=True)
    revgeo          = CharField(null=True)

class Waypoint(PostgresqlModel):
    topic           = BlobField(null=False)
    username        = CharField(null=False)
    device          = CharField(null=False)
    lat             = CharField(null=False)
    lon             = CharField(null=False)
    tst             = DateTimeField(default=datetime.datetime.now)
    rad             = CharField(null=True)
    waypoint        = CharField(null=True)

    class Meta:
        indexes = (
            # Create a unique index on tst
            (('tst', ), True),
        )

if __name__ == '__main__':
    pgsql_db.connect()

    try:
        Location.create_table(fail_silently=True)
    except Exception, e:
        print str(e)

    try:
        Waypoint.create_table(fail_silently=True)
    except Exception, e:
        print str(e)

