--DataOps model using dbt_utils package.
SELECT
    {{ dbt_utils.generate_surrogate_key(['campaign_id', 'date'])}} AS mrkt_spend_uid,
    date                                                           AS cost_dt,
    campaign_id                                                    AS source_campaign_id,
    campaign_nm                                                    AS source_campaign_nm,
    sub_channel                                                    AS source_nm,
    daily_spend                                                    AS cost_amt,
    'DataOps'                                                      AS record_created_by_nm,
    {{ created_or_modified_ts() }}                                 AS record_created_ts
FROM
    {{ ref('facebook_ads_costs_cte') }}

UNION

SELECT
    {{ dbt_utils.generate_surrogate_key(['campaign_id', 'date'])}} AS mrkt_spend_uid,
    date                                                           AS cost_dt,
    campaign_id                                                    AS source_campaign_id,
    campaign_nm                                                    AS source_campaign_nm,
    sub_channel                                                    AS source_nm,
    daily_spend                                                    AS cost_amt,
    'DataOps'                                                      AS record_created_by_nm,
    {{ created_or_modified_ts() }}                                 AS record_created_ts
FROM
    {{ ref('google_ads_costs_cte') }}

UNION

SELECT
    {{ dbt_utils.generate_surrogate_key(['campaign_id', 'date'])}} AS mrkt_spend_uid,
    date                                                           AS cost_dt,
    campaign_id                                                    AS source_campaign_id,
    campaign_nm                                                    AS source_campaign_nm,
    sub_channel                                                    AS source_nm,
    daily_spend                                                    AS cost_amt,
    'DataOps'                                                      AS record_created_by_nm,
    {{ created_or_modified_ts() }}                                 AS record_created_ts
FROM
    {{ ref('linkedin_ads_costs_cte') }}