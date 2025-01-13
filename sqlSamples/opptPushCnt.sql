SELECT
    opportunity_id AS id,
    COUNT(*)       AS my_count --This counts how many times the close date is changed.
FROM
    {{ source('staging_salesforce', 'OPPORTUNITY_FIELD_HISTORY') }}
WHERE
      field = 'CloseDate'
GROUP BY
    opportunity_id