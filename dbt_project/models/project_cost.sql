-- models/project_cost.sql
{{ config(
    materialized='table',
    schema='public'
) }}

-- Store in local Docker PostgreSQL
WITH invoice_source_data AS (
    SELECT
        i.payload::json->>'department' AS department,
        i.payload::json->>'currency' AS currency,
        (i.payload::json->>'amount')::NUMERIC AS amount
    FROM {{ ref('stg_invoice') }} i
)

SELECT
  department,
  SUM(amount) AS total_cost,
  currency
FROM
  invoice_source_data
GROUP BY
  department, currency
