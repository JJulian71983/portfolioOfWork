SELECT DISTINCT
    id,
    IFF(id = FIRST_VALUE(id) OVER (PARTITION BY ultimate_parent_account ORDER BY close_date), TRUE, FALSE) AS first_oppt,
    FIRST_VALUE(id) OVER (PARTITION BY ultimate_parent_account ORDER BY close_date)                        AS first_id
FROM
    (
        SELECT DISTINCT
            opportunity.id,
            account.ultimate_parent_account,
            opportunity.close_date
        FROM
            {{ ref('sf_opportunity_cte') }} opportunity
            LEFT JOIN
                {{ ref('sf_account_cte') }} account
                    ON opportunity.account_id = account.account_id
        WHERE
                opportunity.stage_name IN ('Closed Won - 100%', 'Booked - 99%')
            AND opportunity.record_type_name <> 'Pilot'
    )