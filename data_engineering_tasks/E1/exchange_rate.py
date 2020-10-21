import os
import psycopg2
import psycopg2.extras
import pandas as pd
from dotenv import load_dotenv

# Constants
load_dotenv()
eur_backfill_endpoint = os.environ["EUR_BACKFILL_ENDPOINT"]

connection = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = connection.cursor()

# QUERY TO PULL DATA
combine ="""
WITH Conversion AS (
    SELECT 
    usd_table.currency AS usd_currency, 
    usd_table.rate AS usd_rate, 
    usd_table.date AS usd_date,
    eur_table.currency AS eur_currency, 
    eur_table.rate AS eur_rate, 
    eur_table.date AS eur_date
    FROM usd_table 
    INNER JOIN eur_table
    ON usd_table.pkey = eur_table.pkey
    WHERE usd_table.date > '2020-10-15'
)

SELECT 
    eur_date AS base_date,
    usd_date AS convert_date,
    usd_currency AS currencies,
    usd_rate AS US_Dollar,
    eur_rate AS Euro,
    CAST (100 * eur_rate AS NUMERIC (14, 2)) AS EUR_Conversion,
    CAST (100 * usd_rate AS NUMERIC (14, 2)) AS USD_Conversion
FROM Conversion
"""
# PULL DATA IN FOR CALCULATING ALL CONVERSIONS
cursor.execute(combine)
records = cursor.fetchall()


# PIVOT THE TABLE TO CALCULATE ON THE FLY
currencies = pd.read_sql_query(combine, connection)
usd_currency = currencies.pivot(index='convert_date', columns='currencies', values='us_dollar')
eur_currency = currencies.pivot(index='convert_date', columns='currencies', values='euro')

# GENERATE A TABLE
options = ["EUR", "GBP", "RUB", "ALL CURRENCIES * 100"]
for i in range(len(options)):
    print(str(i+1) + ":", options[i])

curr_input = int(input("Enter a number: "))
if curr_input in range(1, 5):
    curr_input = options[curr_input-1]
else:
    print("Please enter a number between 1 and 4")

# Establish inputs and calculate on the fly
Base = usd_currency['USD']
print('USD Base' + str(Base) + '\n')

if curr_input == "EUR":
    Target_Euro = int(input('Amount USD to Euro: ')) * eur_currency['USD']
    print("Euro Conversion " + '\n'  + str(Target_Euro) + '\n')

if curr_input == "RUB":
    Target_Rub = int(input('Amount USD to Ruble: ')) * eur_currency['RUB']
    print("Ruble Conversion " + '\n' + str(Target_Rub) + '\n')

if curr_input == "GBP":
    Target_Gbp = int(input('Amount USD to U.K. Pound: ')) * eur_currency['GBP']
    print("U.K. Pound Conversion " + '\n' + str(Target_Gbp) + '\n')


if curr_input == "ALL CURRENCIES * 100":
    for row in records:
        currencies = row[2]
        euro_conversion = row[4]
        usd_conversion = row[5]

        print("US Dollar Exchange Rates = " + str(currencies) + ' ' + str(usd_conversion))
        print("Euro Exchange Rates = " + str(currencies) + ' ' + str(euro_conversion), "\n")