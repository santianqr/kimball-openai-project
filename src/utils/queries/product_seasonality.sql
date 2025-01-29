WITH customer_spending AS (
    SELECT 
        c.customer_id,
        d.country,
        COUNT(DISTINCT f.invoice) AS total_purchases,
        SUM(f.total_price) AS total_spent
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_id = c.customer_id
    JOIN dim_country d ON c.country = d.country
    GROUP BY c.customer_id, d.country
)
SELECT 
    customer_id,
    country,
    total_purchases,
    total_spent,
    CASE 
        WHEN total_spent > 5000 THEN 'VIP'
        WHEN total_spent BETWEEN 1000 AND 5000 THEN 'Regular'
        ELSE 'Occasional'
    END AS customer_segment
FROM customer_spending
ORDER BY total_spent DESC;