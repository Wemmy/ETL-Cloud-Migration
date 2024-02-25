-- DROP TABLE IF EXISTS stock;

-- Create stock table 
CREATE TABLE stock(
	date DATE,
	ticker VARCHAR(4),
	open MONEY,
	high MONEY,
	low MONEY,
	close MONEY,
	adj_close MONEY,
	volume INT
	-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Audit column
    -- created_by VARCHAR(50)                            -- Audit column    
);

-- Create cashflow table 
CREATE TABLE cashflow(
	date DATE,
	ticker VARCHAR(4),
	operating_cashflow MONEY,
	investing_cashflow MONEY,
	financial_cashflow MONEY,
	end_cash_position MONEY,
	capital_expenditure MONEY, 
	issuance_of_debt MONEY,
    repayment_of_debt MONEY,
	free_cashflow MONEY
	-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Audit column
    -- created_by VARCHAR(50)                            -- Audit column    
);
