select * from walmart_sales;

-- creating a new dim store

CREATE TABLE IF NOT EXISTS dim_store (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(50) NOT NULL,
    sales_tier VARCHAR(20),
    performance_category VARCHAR(30)
);

INSERT INTO dim_store (store_id, store_name)
SELECT DISTINCT 
    store AS store_id,
    CONCAT('Store #', LPAD(store, 2, '0')) AS store_name
FROM walmart_sales
ORDER BY store_id ASC;

-- Calculate store sales performance tiers
UPDATE dim_store s
JOIN (
    SELECT 
        store,
        AVG(weekly_sales) AS avg_sales
    FROM walmart_sales
    GROUP BY store
) metrics ON s.store_id = metrics.store
SET 
    s.sales_tier = CASE 
        WHEN metrics.avg_sales >= 1500000 THEN 'Tier 1 (High Volume)'
        WHEN metrics.avg_sales >= 1000000 THEN 'Tier 2 (Mid Volume)'
        ELSE 'Tier 3 (Low Volume)'
    END,
    s.performance_category = CASE 
        WHEN metrics.avg_sales >= 1500000 THEN 'Top 25% Outperformer'
        WHEN metrics.avg_sales >= 1000000 THEN 'Average Performer'
        ELSE 'Underperformer / Focus Area'
    END
WHERE s.store_id > 0; -- Explicit primary key check satisfies safe mode

SELECT * FROM dim_store ORDER BY store_id;

-- creating a new dim for date

CREATE TABLE IF NOT EXISTS dim_date (
Date_id INT PRIMARY KEY,
Full_date DATE UNIQUE NOT NULL,
Quarter_num INT NOT NULL,
Month_num INT NOT NULL,
Week_of_year INT NOT NULL,
Year_num INT NOT NULL,
Holiday_flag BOOLEAN NOT NULL,
Holiday VARCHAR(15)
);

INSERT INTO dim_date (Date_id, Full_date,Year_num, Quarter_num, Month_num, Week_of_year,  Holiday_flag)
SELECT DISTINCT
CAST(DATE_FORMAT(STR_TO_DATE(date, '%d-%m-%Y'), '%Y%m%d') AS UNSIGNED) AS Date_id,
STR_TO_DATE(date, '%d-%m-%Y') AS Full_date,
YEAR(STR_TO_DATE(date, '%d-%m-%Y')) AS Year_num,
QUARTER(STR_TO_DATE(date, '%d-%m-%Y')) AS Quarter_num,
MONTH(STR_TO_DATE(date, '%d-%m-%Y')) AS Month_num,
WEEK(STR_TO_DATE(date, '%d-%m-%Y'), 3) AS Week_of_year,
Holiday_flag as Holiday_flag
FROM walmart_sales
ORDER BY full_date ASC;


-- Update specific holiday names by matching exact week-ending dates
UPDATE dim_date
SET Holiday = CASE 
    -- 2010 Holidays
    WHEN full_date = '2010-02-12' THEN 'Super Bowl'
    WHEN full_date = '2010-09-10' THEN 'Labor Day'
    WHEN full_date = '2010-11-26' THEN 'Thanksgiving'
    WHEN full_date = '2010-12-31' THEN 'Christmas'
    
    -- 2011 Holidays
    WHEN full_date = '2011-02-11' THEN 'Super Bowl'
    WHEN full_date = '2011-09-09' THEN 'Labor Day'
    WHEN full_date = '2011-11-25' THEN 'Thanksgiving'
    WHEN full_date = '2011-12-30' THEN 'Christmas'
    
    -- 2012 Holidays
    WHEN full_date = '2012-02-10' THEN 'Super Bowl'
    WHEN full_date = '2012-09-07' THEN 'Labor Day'
    WHEN full_date = '2012-11-23' THEN 'Thanksgiving'
    WHEN full_date = '2012-12-28' THEN 'Christmas'
    
    ELSE 'None'
END
WHERE Date_id > 0;

SELECT * FROM dim_date
where Holiday_flag = 1;


-- creating fact table
CREATE TABLE IF NOT EXISTS fact_weekly_sales (
sales_id INT PRIMARY KEY AUTO_INCREMENT,
date_id INT NOT NULL,
store_id INT NOT NULL,
weekly_sales DECIMAL(12, 2) NOT NULL,
temperature DECIMAL(5, 2),
fuel_price DECIMAL(5, 3),
cpi DECIMAL(8, 4),
unemployment DECIMAL(5, 2),
CONSTRAINT fk_fact_store FOREIGN KEY (store_id) REFERENCES dim_store(store_id),
CONSTRAINT fk_fact_date FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

INSERT INTO fact_weekly_sales (
    store_id,
    date_id,
    weekly_sales,
    temperature,
    fuel_price,
    cpi,
    unemployment
)
SELECT 
    w.store AS store_id,
    d.date_id,
    CAST(w.weekly_sales AS DECIMAL(12, 2)) AS weekly_sales,
    CAST(w.temperature AS DECIMAL(5, 2)) AS temperature,
    CAST(w.fuel_price AS DECIMAL(5, 3)) AS fuel_price,
    CAST(w.cpi AS DECIMAL(8, 4)) AS cpi,
    CAST(w.unemployment AS DECIMAL(5, 2)) AS unemployment
FROM walmart_sales w
JOIN dim_date d 
    ON d.full_date = STR_TO_DATE(w.date, '%d-%m-%Y')
ORDER BY d.date_id ASC, w.store ASC;

SELECT 
    f.sales_id,
    s.store_name,
    s.sales_tier,
    d.full_date,
    d.Holiday AS holiday_name,
    f.weekly_sales,
    f.unemployment
FROM fact_weekly_sales f
JOIN dim_store s ON f.store_id = s.store_id
JOIN dim_date d ON f.date_id = d.date_id
LIMIT 10;

