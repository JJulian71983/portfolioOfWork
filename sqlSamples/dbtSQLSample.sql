/*
This is a DBT SQL example using ephemeral models, Salesforce data, and Snowflake.
*/
SELECT
    IFNULL(account.id, 'MissingAccountID')              AS account_id,
    IFNULL(account.account_name, 'MissingAccountName')  AS account_nm,
    TO_NUMBER(opportunity.arr_cpq, 36, 2)               AS arr_amt,
    opportunity.bdr_owner                               AS bdr_owner_id,
    bdr_owner.name                                      AS bdr_owner_nm,
    calculated_owner_manager.email                      AS calculated_manager_email_address_txt,
    calculated_owner_manager.id                         AS calculated_manager_id,
    calculated_owner_manager.name                       AS calculated_manager_nm,
    calculated_own.email                                AS calculated_owner_email_address_txt,
    opportunity.calculated_owner_id                     AS calculated_owner_id,
    calculated_own.name                                 AS calculated_owner_nm,
    campaign.name                                       AS campaign_type_nm,
    change_count_qtr.push_qtr_count                     AS change_count_qtr,
    opportunity.channel_manager                         AS channel_manager_id,
    channel_manager.name                                AS channel_manager_nm,
    DATE_TRUNC('QUARTER', opportunity.close_date)       AS close_quarter_dt,
    opportunity.close_date                              AS close_dt,
    IFNULL(my_push.my_count, 0)                         AS close_date_change_cnt,
    opportunity.push_count                              AS close_date_push_cnt,
    contact.created_date                                AS contact_created_dt,
    DATE_TRUNC('QUARTER', opportunity.created_date)     AS created_quarter_dt,
    account.csm_id                                      AS csm_id,
    account.csm_nm                                      AS csm_nm,
    opportunity.forecast_category_name                  AS forecast_category_nm,
    opportunity.is_closed                               AS oppt_closed_ind,
    COALESCE(
            stage_1_entered_date,
            stage_2_entered_date,
            stage_3_entered_date,
            stage_4_entered_date,
            stage_5_entered_date
    )                                                   AS initial_progression_dt,
    account.industry_sector_nm                          AS industry_sector_nm,
    IFF(opportunity.type = 'New Business', TRUE, FALSE) AS new_oppt_ind,
    IFF(logo_list.first_oppt = TRUE, TRUE, FALSE)       AS new_logo_ind,
    opportunity.is_pilot                                AS pilot_ind,
    opportunity.is_won                                  AS oppt_won_ind,
    opportunity.lead_category                           AS lead_category_nm,
    opportunity.lead_source                             AS lead_source_nm,
    lead.id                                             AS lead_id,
    opportunity.pilot_source_opportunity                AS pilot_id,
    lead.created_date                                   AS lead_created_dt,
    opportunity.number_of_units_cpq                     AS units_cnt,
    opportunity.created_date                            AS oppt_created_dt,
    opportunity.oppt_name                               AS oppt_nm,
    owner_manager.name                                  AS oppt_owner_manager_nm,
    opportunity_owner.name                              AS oppt_owner_nm,
    opportunity.quota_retirement                        AS quota_retirement_amt,
    opportunity.record_type_id                          AS record_type_id,
    opportunity.record_type_name                        AS record_type_nm,
    account.sales_segment                               AS sales_segment_nm,
    opportunity.campaign_id                             AS salesforce_campaign_id,
    campaign.name                                       AS salesforce_campaign_nm,
    opportunity.owner_id                                AS oppt_owner_id,
    opportunity.id                                      AS oppt_id,
    opportunity.type                                    AS oppt_type_nm,
    'Salesforce'                                        AS source_nm,
    opportunity.stage_name                              AS stage_nm,
    account.sub_vertical                                AS sub_vertical_nm,
    account.vertical_picklist                           AS vertical_nm,
    'DataOps'                                           AS record_created_by_nm,
    CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP())        AS record_created_ts,
    'DataOps'                                           AS record_modified_by_nm,
    CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP())        AS record_modified_ts
FROM
    {{ ref("oppt_cte") }} opportunity
LEFT JOIN
    {{ ref("oppt_account") }} account
    ON opportunity.account_id = account.id
LEFT JOIN
    {{ ref("oppt_lead") }} lead
    ON opportunity.id = lead.converted_opportunity_id
LEFT JOIN
    {{ ref("sf_user_cte") }} opportunity_owner
    ON opportunity.owner_id = opportunity_owner.id
LEFT JOIN
    {{ ref("sf_user_cte") }} calculated_own
    ON opportunity.calculated_owner_id = calculated_own.id
LEFT JOIN
    {{ ref("sf_user_cte") }} bdr_owner
    ON opportunity.bdr_owner = bdr_owner.id
LEFT JOIN
    {{ ref("sf_user_cte") }} calculated_owner_manager
    ON calculated_own.manager_id = calculated_owner_manager.id
LEFT JOIN
    {{ source("staging_salesforce", "CAMPAIGN") }} campaign
    ON opportunity.campaign_id = campaign.id
LEFT JOIN
    {{ ref("sf_user_cte") }} channel_manager
    ON opportunity.channel_manager = channel_manager.id
LEFT JOIN
    {{ ref("logo_list") }} logo_list
    ON opportunity.id = logo_list.id
LEFT JOIN
    {{ ref("sf_user_cte") }} owner_manager
    ON opportunity_owner.manager_id = owner_manager.id
LEFT JOIN
    {{ ref('contact_cte') }} contact
    ON opportunity.contact_id = contact.id
LEFT JOIN
    {{ ref("oppt_push_cnt") }} my_push
    ON opportunity.id = my_push.id
LEFT JOIN
    {{ ref("change_count_qtr") }} change_count_qtr
    ON opportunity.id = change_count_qtr.id
LEFT JOIN
    {{ ref('pilot_units') }} pilot_units
    ON opportunity.id = pilot_units.salesforce_opportunity_id
