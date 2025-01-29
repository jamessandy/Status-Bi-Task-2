-- models/repository_activity.sql
{{ config(
    materialized='table',
    schema='public'
) }}

-- Store in local Docker PostgreSQL
WITH commit_activity AS (
  SELECT
    r.full_name AS repository_name,
    COUNT(c.commit) AS commit_count
  FROM
    {{ ref('stg_commits') }} c
  JOIN
    {{ ref('stg_repositories') }} r
    ON c.repository = r.full_name
  GROUP BY
    r.full_name
),
issue_activity AS (
  SELECT
    r.full_name AS repository_name,
    COUNT(i.id) AS issue_count
  FROM
    {{ ref('stg_issues') }} i
  JOIN
    {{ ref('stg_repositories') }} r
    ON i.repository = r.full_name
  GROUP BY
    r.full_name
),
pr_activity AS (
  SELECT
    r.full_name AS repository_name,
    COUNT(pr.id) AS pr_count
  FROM
    {{ ref('stg_pull_requests') }} pr
  JOIN
    {{ ref('stg_repositories') }} r
    ON pr.repository = r.full_name
  GROUP BY
    r.full_name
)
SELECT
  c.repository_name,
  c.commit_count,
  i.issue_count,
  pr.pr_count
FROM
  commit_activity c
LEFT JOIN
  issue_activity i ON c.repository_name = i.repository_name
LEFT JOIN
  pr_activity pr ON c.repository_name = pr.repository_name