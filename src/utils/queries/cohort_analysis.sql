WITH first_purchase AS (
    -- Determine the first month each customer made a purchase
    SELECT 
        f.customer_id, 
        MIN(DATE_TRUNC('month', d.invoice_date)) AS first_purchase_month
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id  -- Join with dim_date to get actual invoice date
    GROUP BY f.customer_id
),
cohort_analysis AS (
    -- Count how many customers made purchases in each subsequent month after their first purchase
    SELECT 
        f.customer_id,
        fp.first_purchase_month,
        DATE_TRUNC('month', d.invoice_date) AS current_purchase_month,
        EXTRACT(YEAR FROM DATE_TRUNC('month', d.invoice_date)) * 12 + EXTRACT(MONTH FROM DATE_TRUNC('month', d.invoice_date)) -
        (EXTRACT(YEAR FROM fp.first_purchase_month) * 12 + EXTRACT(MONTH FROM fp.first_purchase_month)) AS cohort_month
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id  -- Join to bring the invoice date
    JOIN first_purchase fp ON f.customer_id = fp.customer_id
)
SELECT 
    first_purchase_month,
    cohort_month,
    COUNT(DISTINCT customer_id) AS retained_customers
FROM cohort_analysis
GROUP BY first_purchase_month, cohort_month
ORDER BY first_purchase_month, cohort_month;
