WITH product_sales AS (
    -- Calculamos el total de ventas y número de facturas en las que aparece cada producto
    SELECT 
        p.description AS product_name,
        COUNT(DISTINCT f.invoice) AS total_invoices,
        SUM(f.total_price) AS total_revenue
    FROM fact_sales f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.description
),
top_20_products AS (
    -- Seleccionamos el Top 20 de productos con más revenue
    SELECT * 
    FROM product_sales
    ORDER BY total_revenue DESC
    LIMIT 20
),
stats AS (
    -- Calculamos la media y la desviación estándar del número de facturas
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
        WHEN t.total_invoices < (s.avg_invoices - s.std_invoices) THEN 'Q1 - Bajo'
        WHEN t.total_invoices BETWEEN (s.avg_invoices - s.std_invoices) AND s.avg_invoices THEN 'Q2 - Medio-Bajo'
        WHEN t.total_invoices BETWEEN s.avg_invoices AND (s.avg_invoices + s.std_invoices) THEN 'Q3 - Medio-Alto'
        ELSE 'Q4 - Alto'
    END AS quartile
FROM top_20_products t
CROSS JOIN stats s
ORDER BY total_revenue DESC;
