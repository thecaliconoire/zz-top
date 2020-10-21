import requests
import os
import psycopg2
import psycopg2.extras 
import datetime
from dotenv import load_dotenv

# Constants
load_dotenv()
eur_backfill_endpoint = os.environ["EUR_BACKFILL_ENDPOINT"]

connection = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = connection.cursor()

# Queries
eur_create = """
CREATE TABLE 
eur_table 
(
    txid serial, 
    pkey varchar PRIMARY KEY, 
    currency varchar, 
    rate real, 
    date date, 
    timestamp timestamp, 
    base varchar
);"""
eur_insert = """
INSERT INTO 
eur_table 
(
    currency, 
    pkey, 
    rate, 
    date, 
    timestamp, 
    base
) 
VALUES ( %s, %s, %s, %s, %s, %s);"""

print("creating table...")

r = requests.get(eur_backfill_endpoint)
response = r.json()
cursor.execute(eur_create)


# insert EURO data.
for key, value in response.items():
    for key_one, value_one in value.items():
        for key_two, value_two in value_one.items():
            timestamp = format(datetime.datetime.now())
            base = response['base']
            date = datetime.datetime.strptime(key_one, '%Y-%m-%d').date()
            currency = key_two
            rate = value_two
            pkey = currency + str(date)
            cursor.execute(eur_insert, (currency, pkey, rate, date, timestamp, base))
            connection.commit()
print("Table Created!")

