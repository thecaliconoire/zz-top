import requests
import os
import psycopg2
import psycopg2.extras 
import datetime
from dotenv import load_dotenv

# Constants
load_dotenv()
usd_backfill_endpoint = os.environ["USD_BACKFILL_ENDPOINT"]

connection = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = connection.cursor()

# Queries
usd_create = """
CREATE TABLE 
    usd_table 
    (txid serial, 
    pkey varchar PRIMARY KEY, 
    currency varchar, 
    rate real, 
    date date, 
    timestamp timestamp, 
    base varchar);"""

usd_insert = """
INSERT INTO 
    usd_table
(
    currency, 
    pkey, 
    rate, 
    date, 
    timestamp, 
    base
) 
VALUES (%s, %s, %s, %s, %s, %s);"""
print("creating table...")

r = requests.get(usd_backfill_endpoint)
response = r.json()
cursor.execute(usd_create)

# insert USD data.
for key, value in response.items():
    for key_one, value_one in value.items():
        for key_two, value_two in value_one.items():
            timestamp = format(datetime.datetime.now())
            base = response['base']
            date = datetime.datetime.strptime(key_one, '%Y-%m-%d').date()
            currency = key_two
            rate = value_two
            pkey = currency + str(date)
            cursor.execute(usd_insert, (currency, pkey, rate, date, timestamp, base))
            connection.commit()
    


cursor.execute(select)
records = cursor.fetchall()

for row in records:
   print(row[0])
   print("date = ", row[0] )
   print("currency = ", row[1])
   print("rate  = ", row[2], "\n")