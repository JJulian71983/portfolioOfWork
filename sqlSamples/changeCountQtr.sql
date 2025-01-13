--This is a DBT sample using Salesforce data.
SELECT
    id,
    ARRAY_AGG(push_qtr_count) AS push_qtr_count --these are the dates, as an array, of each close date push. This is used in the Project Oxygen ind aggregations to join the above close date change metric.
FROM
    (
        SELECT
            opportunity_id AS id,
            OBJECT_CONSTRUCT(TO_VARCHAR(TO_DATE(DATE_TRUNC('QUARTER', created_ts))), COUNT(*)) AS push_qtr_count
        FROM
            {{ source('staging_salesforce', 'OPPORTUNITY_FIELD_HISTORY') }}
        WHERE
              field = 'CloseDate'
        GROUP BY
            opportunity_id,
            TO_DATE(DATE_TRUNC('QUARTER', created_ts))
    )
GROUP BY
    id