SELECT
    salesforce_opportunity_id,
    IFNULL(COUNT(task_nr, 0), 0) AS pilots
FROM
    {{ ref("implementation_data") }}
WHERE
    pilot_onboarding_ind = true
    AND configuration_dt IS NULL
GROUP BY
    salesforce_opportunity_id