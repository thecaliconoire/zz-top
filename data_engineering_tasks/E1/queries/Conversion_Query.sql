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
usd_currency AS USD_Currencies,
usd_rate AS US_Dollar,
eur_rate AS Euro,
CAST (100 * eur_rate AS NUMERIC (14, 2)) AS EUR_Conversion,
CAST (100 * usd_rate AS NUMERIC (14, 2)) AS USD_Conversion
FROM Conversion