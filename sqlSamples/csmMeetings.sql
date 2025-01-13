--A DBT model referencing three ephemeral models. Data source is Salesforce.
SELECT DISTINCT
    id,
    name,
    NULL AS profile_id,
    company
FROM
    {{ ref('sf_lead_cte') }}
UNION
SELECT DISTINCT
    id,
    name,
    NULL AS profile_id,
    NULL AS company
FROM
    {{ ref('sf_contact_cte') }}
UNION
SELECT DISTINCT
    id,
    name,
    profile_id,
    NULL AS company
FROM
    {{ ref('sf_user_cte') }}