-- This query calculates year-over-year sales growth by country using CTEs.
-- It first aggregates total sales by country and year, then computes the percentage growth compared to the previous year.

WITH sales_by_year AS (
    SELECT 
        d.country,  
        dt.year,  
        SUM(f.total_price) AS total_sales  
    FROM fact_sales f
    JOIN dim_country d ON f.country_id = d.country_id  
    JOIN dim_date dt ON f.date_id = dt.date_id 
    GROUP BY d.country, dt.year
),

-- CTE to calculate year-over-year sales growth
sales_growth AS (
    SELECT 
        s1.country,  
        s1.year AS current_year,  
        s1.total_sales AS sales_current_year,  
        s2.total_sales AS sales_previous_year,
        ROUND(
            ( (s1.total_sales - s2.total_sales) / NULLIF(s2.total_sales, 0) )::NUMERIC * 100, 2
        ) || '%' AS growth_percentage
    FROM sales_by_year s1
    LEFT JOIN sales_by_year s2 
    ON s1.country = s2.country AND s1.year = s2.year + 1 
)

-- Selecting only records where previous year's sales exist to ensure valid growth calculation
SELECT * FROM sales_growth
WHERE sales_previous_year IS NOT NULL
ORDER BY growth_percentage DESC;