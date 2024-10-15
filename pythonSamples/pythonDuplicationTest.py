# This python script checks for duplicate rows as defined by the SELECT statement for Snowflake. A sample can be taken by adjusting the Bernoulli percent.
import snowflake.snowpark as snowpark

def main(session: snowpark.Session):
    duplicate_check_df = session.sql(query = "SELECT * FROM DB.SCHEMA.TABLE TABLESAMPLE BERNOULLI (100)").to_pandas()
    has_duplicates = duplicate_check_df.duplicated()
    for dup in has_duplicates:
        if dup:
            print(dup)
            return dup
        else:
            pass
    return False