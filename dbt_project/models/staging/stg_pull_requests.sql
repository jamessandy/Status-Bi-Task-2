{{ config(
    materialized='table',
    schema='public'
) }}

SELECT * FROM {{ source('local_github', 'pull_requests') }}