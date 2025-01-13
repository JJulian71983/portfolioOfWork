SELECT
    {{ dbt_utils.generate_surrogate_key(
        [
            'order_cte.order_id',
            'order_item_cte.id',
            'order_cte.account_id',
            'order_cte.quote_id',
            'order_item_cte.product_id'
            ]
                                            )
                                                }}                 AS uid,
    order_cte.billing_backfill                                     AS needs_backfill_ind,
    billing_acct_cte.account_name                                  AS billable_client_nm,
    billing_acct_cte.customer_id                                   AS billable_client_uuid,
    order_cte.order_id,
    order_cte.opportunity_id,
    loc_acct_cte.account_name                                      AS shipping_account_nm,
    loc_acct_cte.shipping_account_address_nm,
    order_cte.activated_mountain_ts                                AS order_activated_ts,
    oppt_cte.close_dt,
    oppt_cte.csm_nm,
    contract_cte.contract_start_dt,
    contract_cte.contract_end_dt,
    TO_NUMBER(order_item_cte.product_acumatica_external_id, 38, 0) AS sku_id,
    order_item_cte.product_nm,
    order_item_cte.id                                              AS product_id,
    subscription_cte.subscription_start_dt,
    subscription_cte.subscription_end_dt,
    TO_NUMBER(order_item_cte.quantity, 36, 0)                      AS quantity_cnt,
    TO_NUMBER(order_item_cte.unit_price, 36, 2)                    AS unit_price_amt,
    TO_NUMBER(order_item_cte.monthly_per_unit_price, 36, 2)        AS monthly_per_unit_price_amt,
    order_cte.vms_true_up                                          AS vms_true_up_dt,
    'DataOps'                                                      AS record_created_by_nm,
    {{ created_or_modified_ts() }}                                 AS record_created_ts
FROM
    {{ ref('sf_order_cte') }} order_cte
    LEFT JOIN
        {{ ref('sf_order_item_cte') }} order_item_cte
        ON order_cte.order_id = order_item_cte.order_id
    LEFT JOIN
        {{ ref('sf_account_cte') }} acct_cte
        ON order_cte.account_id = acct_cte.account_id
    LEFT JOIN
        {{ ref('sf_loc_acct_cte') }} loc_acct_cte
        ON order_cte.ship_to_account_id = loc_acct_cte.account_id
    LEFT JOIN
        (
            SELECT
                contract_start_dt,
                contract_end_dt,
                order_id
            FROM
                {{ ref('sf_contract_cte') }}
            WHERE
                latest_contract_for_order_ind = TRUE
         ) contract_cte
        ON order_item_cte.order_id = contract_cte.order_id
    LEFT JOIN
        {{ ref('sf_subscription_cte') }} subscription_cte
        ON order_item_cte.subscription_id = subscription_cte.subscription_id
    LEFT JOIN
        {{ ref('sf_account_cte') }} billing_acct_cte
        ON order_cte.billing_account_id = billing_acct_cte.account_id
    LEFT JOIN
        {{ ref('opportunity') }} oppt_cte
        ON order_cte.opportunity_id = oppt_cte.oppt_id