SELECT
    lead_id,
    SUM(opportunity_arr)                                                                                      AS arr_amt,
    SUM(IFF(sort_order IN (15, 16) ,units, 0))                                                                AS booked_units_cnt, --15 and 16 are the new sort order for the booked stages. Using this instead of labels because they have changed frequently.
    ANY_VALUE(converted_account_id)                                                                           AS converted_account_id,
    ANY_VALUE(converted_contact_id)                                                                           AS converted_contact_id,
    ANY_VALUE(salesforce_created_dt)                                                                          AS created_dt,
    ANY_VALUE(hubspot_contact_id)                                                                             AS hubspot_contact_id,
    ANY_VALUE(hubspot_created_dt)                                                                             AS hubspot_created_dt,
    ANY_VALUE(lead_category_nm)                                                                               AS lead_category_nm,
    ANY_VALUE(lead_nm)                                                                                        AS lead_nm,
    ANY_VALUE(marketing_lifecycle_stage_nm)                                                                   AS marketing_lifecycle_stage_nm,
    COUNT(opportunity_id)                                                                                     AS opportunity_cnt,
    ANY_VALUE(segment_nm)                                                                                     AS segment_nm,
    ANY_VALUE(source_nm)                                                                                      AS source_nm,
    AVG(creation_to_stage_1)                                                                                  AS stage_0_to_1_avg_days_cnt,
    COUNT_IF(sort_order NOT IN (7, 14) OR (sort_order = 14 AND stage_at_close_order <> 7))                    AS stage_1_oppt_cnt,
    AVG(stage_1_to_booked)                                                                                    AS stage_1_to_booked_avg_days_cnt,
    ANY_VALUE(sub_vertical_nm)                                                                                AS sub_vertical_nm,
    ANY_VALUE(utm_campaign_nm)                                                                                AS utm_campaign_nm,
    ANY_VALUE(utm_source_nm)                                                                                  AS utm_source_nm,
    ANY_VALUE(vertical)                                                                                       AS vertical_nm,
    'DataOps'                                                                                                 AS record_created_by_nm,
    CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP())                                                              AS record_created_ts
FROM
    {{ ref('lead_progress_details') }}
GROUP BY
    lead_id