-- 1. Total visits by department
SELECT dep.department_name, COUNT(*) AS total_visits
FROM fact_visits f
JOIN dim_department dep ON f.department_id = dep.department_id
GROUP BY dep.department_name
ORDER BY total_visits DESC;

-- 2. Total visits by year
SELECT d.year, COUNT(*) AS total_visits
FROM fact_visits f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;

-- 3. Average treatment cost by disease
SELECT dis.disease_name, AVG(f.cost) AS avg_cost
FROM fact_visits f
JOIN dim_disease dis ON f.disease_id = dis.disease_id
GROUP BY dis.disease_name
ORDER BY avg_cost DESC;

-- 4. Average treatment days by department
SELECT dep.department_name, AVG(f.treatment_days) AS avg_days
FROM fact_visits f
JOIN dim_department dep ON f.department_id = dep.department_id
GROUP BY dep.department_name
ORDER BY avg_days DESC;

-- 5. Drill-down: visits by year and month
SELECT d.year, d.month_name, COUNT(*) AS total_visits
FROM fact_visits f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- 6. Slice: only Cardiology
SELECT d.year, COUNT(*) AS total_visits
FROM fact_visits f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_department dep ON f.department_id = dep.department_id
WHERE dep.department_name = 'Cardiology'
GROUP BY d.year;

-- 7. Dice: Cardiology in 2024 in North region
SELECT COUNT(*) AS total_visits
FROM fact_visits f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_department dep ON f.department_id = dep.department_id
JOIN dim_region r ON f.region_id = r.region_id
WHERE dep.department_name = 'Cardiology'
  AND d.year = 2024
  AND r.region_name = 'North';