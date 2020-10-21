import os
import pytest
import psycopg2
# from pytest_postgresql import factories
from dotenv import load_dotenv
load_dotenv()


@pytest.fixture
def connection():
    """Fixture to set up the in-memory database with test data"""
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE currency(date date, currency varchar, rate real, base varchar);''')
    yield conn

@pytest.fixture
def setup(connection):
    cursor = connection.cursor()
    sample_data = [
        ('2020-01-01', 'USD', '1.178', 'EUR'),
        ('2020-01-01', 'GBP', '2.22', 'EUR'),
        ('2020-01-01', 'EUR', '1', 'EUR')
    ]
    cursor.executemany('''INSERT INTO currency(date, currency, rate, base) VALUES (%s, %s, %s, %s);''', sample_data)
    yield cursor
