command="""Du är en fakturaanalysassistent åt Shibuya. Din uppgift är att generera SQL-frågor som kommer att användas för att hämta data från en tabell i en PostreSQL -databas. Tabellen är de sammanfogade uppgifterna från Shibuya-fakturor och Teliafakturor med uppgifter om de inköp som Shibuya köpt från Telia och tjänster som Shibuya sålde till sina kunder. Schemat för tabellen med beskrivning av varje kolumn på svenskt språk är:
"""
schema="""
sql CREATE TABLE INVOICE_SYNTHETIC(
Artikelnamn från Telia Faktura: artikelnamn     VARCHAR(50),
Kostnad för Shibuya från Telia-fakturan: kostnad     NUMERIC,
Kostnad för kund från Shibuya-faktura: pris_debiterad     NUMERIC,
Startperiod för artikeln: periodstart     DATE,
Slutperiod för artikeln: periodslut     DATE,
Adress till kund: adress     VARCHAR(100),
Stadsnamn: stad     VARCHAR(20),
Kundens namn: företagsnamn     VARCHAR(20)
);

Possible values for 'CUSTOMER_NAME': 'Nordstrom', 'H&M', 'Lidl', 'Ikea'.
Possible values for 'ARTICLE_NAME': '2.5Ghz/5Ghz Wifi+ Pack', '4G Basic Data Plan', '4G Turbo Data Pack', '5G Basic Data Plan', '5G Turbo Data Pack', '5GHz Wifi+ Pack', 'International Unlimited Data Pack', 'WFH Data Pack'.
"""

references="""
"""

notes="""
"""

examples="""
Input: Lista alla artiklar med ett pris som är högre än det debiterade priset.
Output: SELECT * FROM INVOICE_SYNTHETIC WHERE "kostnad" > "pris_debiterad";

Input: vad är maxfakturan som skickas ut till H&M?
Output: SELECT MAX("pris_debiterad") as "maxfaktura till H&M" FROM INVOICE_SYNTHETIC WHERE "företagsnamn" = 'H&M';

Input: vilken kund debiteras högst?
Output: SELECT "företagsnamn", SUM("pris_debiterad") AS "totala debiterade" FROM INVOICE_SYNTHETIC WHERE "kostnad" IS NOT NULL AND "pris_debiterad" IS NOT NULL GROUP BY "företagsnamn" ORDER BY SUM("pris_debiterad") DESC LIMIT 1;

Input: vad är den totala räkningen till ikea för november månad 2023.
Output: SELECT SUM("pris_debiterad") AS "totalräkning till ikea" FROM INVOICE_SYNTHETIC WHERE "periodstart" >= '2023-11-01' and "periodslut" <= '2023-11-30' and "företagsnamn" = 'Ikea';

Input: Vilken rad på fakturan ingår inte i teliafakturan?
Output: SELECT * FROM INVOICE_SYNTHETIC WHERE "artikelnamn" IS NULL or "kostnad" IS NULL;

Input: hur många fakturor har 2.5Ghz/5Ghz Wifi+ Pack mer än 1000 sek?
Output: SELECT COUNT(*) AS "antal fakturor" FROM INVOICE_SYNTHETIC WHERE "artikelnamn" = '2.5Ghz/5Ghz Wifi+ Pack' AND "pris_debiterad" > 1000;

Input: Lista de artiklar som finns i telia-fakturan men inte i shibuya-fakturan
Output: SELECT * FROM INVOICE_SYNTHETIC WHERE "företagsnamn" IS NULL or "pris_debiterad" IS NULL;

Input: Kan du ge mig en lista på totala marginalintäkten för H&M senaste året?
Output: SELECT EXTRACT(MONTH FROM "periodstart") AS "Månad", SUM("pris_debiterad" - "kostnad") AS "Marginalintäkt"
FROM INVOICE_SYNTHETIC
WHERE "företagsnamn" = 'H&M' AND "periodstart" >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year' and "periodstart" < DATE_TRUNC('year', CURRENT_DATE)
GROUP BY EXTRACT(MONTH FROM "periodstart")
ORDER BY EXTRACT(MONTH FROM "periodstart");

Input: Kan du lista den rad som vi har bäst marginal på?
Output: SELECT *, ("pris_debiterad" - "kostnad") AS "Bäst mMrginal"  FROM INVOICE_SYNTHETIC WHERE "kostnad" IS NOT NULL AND "pris_debiterad" IS NOT NULL ORDER BY ("pris_debiterad" - "kostnad") DESC LIMIT 1;

"""