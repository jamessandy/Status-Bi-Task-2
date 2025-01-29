{{ config(
    materialized='table',
    schema='public'
) }}

SELECT * FROM {{ source('local_finance', 'invoice') }}