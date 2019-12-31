import pytest
from MobilityDB import *

db = psycopg2.connect(host='localhost', dbname="mobilitydb", user='mobilitydb', password='')
db.autocommit = True

MobilityDBRegister(db)
cur = db.cursor()

time_types = [TimestampSet, Period, PeriodSet]
duration_suffixes = ['Inst', 'I', 'Seq', 'S']
duration_types = ['INSTANT', 'INSTANTSET', 'SEQUENCE', 'SEQUENCESET']
temporal_types = [TBool, TInt, TFloat, TGeomPoint, TGeogPoint]

def pytest_configure():
	for time in time_types:
		cur.execute(
			'CREATE TABLE IF NOT EXISTS tbl_' + time.__name__.lower() +
			'(timetype ' +  time.__name__.lower() + ' NOT NULL);')
	for ttype in temporal_types:
		for suffix, duration in zip(duration_suffixes, duration_types):
			cur.execute(
				'CREATE TABLE IF NOT EXISTS tbl_' + ttype.__name__.lower() + suffix +
				'(temp ' + ttype.__name__.lower() + '(' + duration + ') NOT NULL);')

def pytest_unconfigure():
	"""
		for temp in temporal_types:
		for ttype in temp:
			cur.execute('DROP TABLE tbl_' + ttype.__name__.lower() + ';')
	"""
	pass

@pytest.fixture
def cursor():
    # Make sure tables are clean.
	for ttype in temporal_types:
		for suffix in duration_suffixes:
			cur.execute('TRUNCATE TABLE tbl_' + ttype.__name__.lower() + suffix + ';')
	return cur
