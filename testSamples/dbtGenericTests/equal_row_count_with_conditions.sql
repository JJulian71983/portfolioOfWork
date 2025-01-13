{% test equal_row_count_with_conditions(model, column_name, compare_model, compare_column_name, condition_sql="1=1", compare_condition_sql="1=1") %}

    WITH model_count AS (
        SELECT
            COUNT({{ column_name }}) AS model_count
        FROM
            {{ model }}
        WHERE
            {{ condition_sql }}
    ),
    compare_model_count AS (
        SELECT
            COUNT({{ compare_column_name }}) AS compare_model_count
        FROM
            {{ compare_model }}
        WHERE
            {{ compare_condition_sql }}
    )
    SELECT
        *
    FROM
        model_count, compare_model_count
    WHERE
        model_count <> compare_model_count

{% endtest %}