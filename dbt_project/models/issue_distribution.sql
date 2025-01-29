-- models/issue_label_distribution.sql
{{ config(
    materialized='table',
    schema='public' 
) }}

-- Store in local Docker PostgreSQL
WITH issue_type_dist AS (
  SELECT
    i.repository AS repository_name,
    split_part(i.title, ':', 1) AS issue_type,
    i.id AS id
  FROM
    {{ ref('stg_issues') }} i
)
SELECT
  repository_name,
  issue_type,
  COUNT(id) AS issue_count
FROM
  issue_type_dist
GROUP BY
  repository_name, issue_type
