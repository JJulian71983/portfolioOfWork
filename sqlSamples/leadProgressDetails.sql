--DBT data mart model that combines several Salesforce objects to produce lead lifecycle data.
SELECT
    sf_lead.id                                                                                                AS lead_id,
    sf_lead.converted_account_id                                                                              AS converted_account_id,
    sf_lead.converted_contact_id                                                                              AS converted_contact_id,
    TO_DATE(hs_contact.create_date)                                                                           AS hubspot_created_dt,
    hs_contact.uid                                                                                            AS hubspot_contact_id,
    sf_lead.name                                                                                              AS lead_nm,
    FIRST_VALUE(sf_opportunity.lead_category)OVER(PARTITION BY sf_lead.id ORDER BY sf_opportunity.created_ts) AS lead_category_nm,
    COALESCE(sf_contact.marketing_lifecycle_stage, sf_lead.marketing_lifecycle_stage)                         AS marketing_lifecycle_stage_nm,
    sf_opportunity.id                                                                                         AS opportunity_id,
    sf_opportunity.arr_cpq                                                                                    AS opportunity_arr,
    TO_DATE(sf_lead.created_ts)                                                                               AS salesforce_created_dt,
    sf_account.sales_segment                                                                                  AS segment_nm,
    sf_opportunity.stage_name                                                                                 AS stage_nm,
    sf_opportunity.stage_at_close_order                                                                       AS stage_at_close_order,
    sf_opportunity.sort_order                                                                                 AS sort_order,
    sf_lead.lead_source                                                                                       AS source_nm,
    sf_account.sub_vertical                                                                                   AS sub_vertical_nm,
    sf_opportunity.number_of_units_cpq                                                                        AS units,
    hs_contact.utm_campaign                                                                                   AS utm_campaign_nm,
    hs_contact.utm_source                                                                                     AS utm_source_nm,
    sf_account.vertical_picklist                                                                              AS vertical,
    DATEDIFF('day', sf_opportunity.created_ts, sf_opportunity.stage_1_entered_date)                           AS creation_to_stage_1,
    DATEDIFF('day', sf_opportunity.stage_1_entered_date, sf_opportunity.stage_5_entered_date)                 AS stage_1_to_booked
FROM
    {{ ref('sf_lead_cte') }} sf_lead
    LEFT JOIN
        (
            SELECT
                create_date,
                uid,
                salesforce_contact_id,
                salesforce_lead_id,
                utm_campaign,
                utm_source
            FROM
                {{ source('staging_hubspot', 'CONTACT') }}
            QUALIFY
                ROW_NUMBER()OVER(PARTITION BY salesforce_lead_id ORDER BY salesforce_last_sync_time DESC) = 1
         ) hs_contact
        ON sf_lead.id = hs_contact.salesforce_lead_id
    LEFT JOIN
        (
            SELECT
                id,
                marketing_lifecycle_stage
            FROM
                {{ ref('sf_contact_cte') }}
        ) sf_contact
        ON sf_lead.converted_contact_id = sf_contact.id AND hs_contact.salesforce_contact_id = sf_contact.id
    LEFT JOIN
        (
            SELECT
                account_id,
                sales_segment,
                vertical_picklist,
                sub_vertical
            FROM
                {{ ref('sf_account_cte') }}
        ) sf_account
        ON sf_lead.converted_account_id = sf_account.account_id
    LEFT JOIN
        (
            SELECT
                oppt.id,
                oppt.account_id,
                oppt.stage_name,
                oppt_stage.sort_order,
                oppt_stage_at_close.sort_order AS stage_at_close_order,
                oppt.contact_id,
                oppt.stage_1_entered_date,
                oppt.stage_2_entered_date,
                oppt.stage_3_entered_date,
                oppt.stage_4_entered_date,
                oppt.stage_5_entered_date,
                oppt.arr_cpq,
                oppt.lead_category,
                oppt.created_ts,
                oppt.number_of_units_cpq
            FROM
                {{ ref('sf_opportunity_cte') }} oppt
                LEFT JOIN
                    (
                        SELECT
                            master_label,
                            sort_order
                        FROM
                            {{ source('staging_salesforce', 'OPPORTUNITY_STAGE') }}
                        WHERE
                            is_active = TRUE
                    ) oppt_stage
                    ON oppt.stage_name = oppt_stage.master_label
                LEFT JOIN
                     (
                        SELECT
                            master_label,
                            sort_order
                        FROM
                            {{ source('staging_salesforce', 'OPPORTUNITY_STAGE') }}
                        WHERE
                            is_active = TRUE
                    ) oppt_stage_at_close
                    ON oppt.stage_at_close = oppt_stage_at_close.master_label
            WHERE
                oppt.record_type_id = '0124W000000fqle5tg'
        ) sf_opportunity
        ON sf_opportunity.contact_id = sf_lead.converted_contact_id