{{ config(materialized='table') }}

SELECT
    post_type_id,
    AVG(score) as avg_score,
    COUNT(*) as total_posts
FROM {{ source('warehouse', 'posts') }}
GROUP BY 1
