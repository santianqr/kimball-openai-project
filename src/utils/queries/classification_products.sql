-- This query analyzes the top 20 products based on total revenue,
-- categorizing them into quartiles based on the number of invoices they appear in.

WITH product_sales AS (
    -- Calculate total sales and the number of invoices each product appears in
    SELECT 
        p.description AS product_name,
        COUNT(DISTINCT f.invoice) AS total_invoices,
        SUM(f.total_price) AS total_revenue
    FROM fact_sales f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.description
),
top_20_products AS (
    -- Select the top 20 products with the highest revenue
    SELECT * 
    FROM product_sales
    ORDER BY total_revenue DESC
    LIMIT 20
),
stats AS (
    -- Calculate the average and standard deviation of the number of invoices
    SELECT 
        AVG(total_invoices) AS avg_invoices,
        STDDEV(total_invoices) AS std_invoices
    FROM top_20_products
)
SELECT 
    t.product_name,
    t.total_invoices,
    t.total_revenue,
    CASE 
        WHEN t.total_invoices < (s.avg_invoices - s.std_invoices) THEN 'Q1 - Low'
        WHEN t.total_invoices BETWEEN (s.avg_invoices - s.std_invoices) AND s.avg_invoices THEN 'Q2 - Medium-Low'
        WHEN t.total_invoices BETWEEN s.avg_invoices AND (s.avg_invoices + s.std_invoices) THEN 'Q3 - Medium-High'
        ELSE 'Q4 - High'
    END AS quartile
FROM top_20_products t
CROSS JOIN stats s
ORDER BY total_revenue DESC;