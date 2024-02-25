-- Copy stock data from CSV file into database
-- COPY stock(date, ticker, open, high, low, close, adj_close, volume)
-- FROM 'C:/Users/WRTP/Documents/Min_Projects/newhorizon_finance/data/stocks.csv'
-- DELIMITER ','
-- ;
\copy stock FROM 'C:/Users/WRTP/Documents/Min_Projects/newhorizon_finance/data/stocks.csv' WITH (FORMAT csv, HEADER,DELIMITER ',');

-- COPY cashflow(date, ticker, operating_cashflow, investing_cashflow, financial_cashflow, 
--               end_cash_position, capital_expenditure, issuance_of_debt, repayment_of_debt, 
-- 		      free_cashflow)
-- FROM 'C:/Users/WRTP/Documents/Min_Projects/newhorizon_finance/data/cashflow.csv'
-- FORMAT csv
-- DELIMITER ','
-- ;
\copy cashflow FROM 'C:/Users/WRTP/Documents/Min_Projects/newhorizon_finance/data/cashflow.csv' WITH (FORMAT csv, HEADER);