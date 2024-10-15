## ADAPTIVE INSIGHTS INGESTION ##
from requests import post
from os import environ
from io import BytesIO
from snowflake.snowpark import session, files
from datetime import datetime
from re import sub
from xml.etree import ElementTree
from pandas import DataFrame


def adaptive_extraction():  # Defining a function so it can be called in the main file when scheduling.
    # Create Snowflake session.
    connection_parameters = {
        "user": environ['SNOWPARK_USER'],  # This is how you handle a DataOps environment variable.
        "password": environ['SNOWPARK_PASSWORD'],
        "account": environ['SNOWPARK_ACCOUNT'],
        "role": environ['SNOWPARK_ROLE'],
        "warehouse": environ['SNOWPARK_WAREHOUSE'],
        "database": environ['SNOWPARK_DATABASE'],
        "schema": environ['SNOWPARK_SCHEMA']
        }
    conn = session.Session.builder.configs(connection_parameters).create()

    # Setting up all needed parameters for the API call to Adaptive.
    caller_name = environ['ADAPTIVE_INSIGHTS_CALLER']
    user_name = environ['ADAPTIVE_INSIGHTS_USER']
    password = environ['ADAPTIVE_INSIGHTS_PASSWORD']
    instance = environ['ADAPTIVE_INSIGHTS_INSTANCE']
    sheet_level = "Top_Level"
    adaptive_sheet = "Custom Accounts"
    file_name_sheet = sub(pattern = "\\s", repl = "_", string = adaptive_sheet)
    sheet_version = "Current Version"
    df_columns = list()
    df_data = list()
    end_month = datetime.now().month
    end_year = datetime.now().year
    if len(str(end_month)) < 2:
        end_month_year = "0" + str(end_month) + "/" + str(end_year)
    else:
        end_month_year = str(end_month) + "/" + str(end_year)
    stage_prefix = str(end_year) + "_" + str(end_month)
    stg_location = f"@{environ['SNOWPARK_DATABASE']}.ADAPTIVE_INSIGHTS.ADAPTIVE_INSIGHTS_CUSTOM_ACCOUNTS/{stage_prefix}_{file_name_sheet}.xml"
    api_version = "v38"  # See https://doc.workday.com/adaptive-planning/en-us/integration/managing-data-integration/api-documentation/cbi1623709771566.html?toc=1.3.0 for version and API docs.
    api_endpoint = "https://api.adaptiveplanning.com/api/"
    full_url = api_endpoint + api_version
    headers = {"accept": "application/xml"}
    data_export = f"""<?xml version='1.0' encoding='UTF-8'?>
    <call method="exportData" callerName="{caller_name}">
        <credentials login="{user_name}" password="{password}" instanceCode="{instance}"/>
        <version name="{sheet_version}"/>
        <format useInternalCodes="true" includeUnmappedItems="false"/>
        <sheet id="401"/>
        <filters>
            <accounts>
                <account code="c_ARR_YoY_Growth" isAssumption="false" includeDescendants="false"/>
                <account code="c_EBITDA_Margin_TTM" isAssumption="false" includeDescendants="false"/>
                <account code="c_CAGR" isAssumption="false" includeDescendants="false"/>
                <account code="c_FCF_Margin_TTM" isAssumption="false" includeDescendants="false"/>
                <account code="c_Churn_Pct" isAssumption="false" includeDescendants="false"/>
                <account code="c_Subscription_GM_TTM" isAssumption="false" includeDescendants="false"/>
                <account code="c_Gross_Dollar_Retention" isAssumption="false" includeDescendants="false"/>
                <account code="c_Net_Dollar_Retention" isAssumption="false" includeDescendants="false"/>
                <account code="c_Is_Forecast" isAssumption="false" includeDescendants="false"/>
            </accounts>
            <levels>
                <level name="{sheet_level}" isRollup="false" includeDescendants="false"/>
            </levels>
            <timeSpan start="01/2023" end="{end_month_year}" stratum="month"/>
        </filters>
        <rules timeRollups="true">
        </rules>
    </call>"""
    # Make the API call to Adaptive then convert the response to bytes to upload it to the stage in Snowflake.
    response = post(url = full_url, data = data_export, headers = headers).text
    response_file = BytesIO(bytes(response, 'utf-8'))
    put_results = conn.file.put_stream(input_stream = response_file, stage_location = stg_location, auto_compress = False, overwrite = True)
    response_file.close()
    # Retrieve XML from stage and set parameters for table creation.
    read_xml = conn.file.get_stream(stage_location = stg_location).read()
    xml_string = read_xml.decode()
    parsed_xml = ElementTree.fromstring(xml_string)
    for child in parsed_xml:
        adaptive_data = child.text
        filter_data = sub(pattern = "\\s", repl = "_", string = sub(pattern = r"\n", repl = ";", string = adaptive_data))
        columns = filter_data.split(sep = ";", maxsplit = 1)[0].upper()
        columns = columns.split(sep = ",")
        for column in columns:
            if column[0] in ["0", "1"]:
                column = "C_" + column
                df_columns.append(column)
            else:
                column = "C_" + sub(pattern = "-", repl = "/", string = column)
                df_columns.append(column)
        data_string = sub(pattern = "\"", repl = "", string = filter_data.split(sep = ";", maxsplit = 1)[1])
        data = data_string.split(sep = ";")
        for dt in data:
            new_dt = dt.split(sep = ",")
            df_data.append(new_dt)
    # Create dataframe to insert data.
    df_to_insert = DataFrame(data = df_data, columns = df_columns)
    # Insert data
    pandas_write_status = conn.write_pandas(df = df_to_insert, table_name = "CUSTOM_ACCOUNTS", schema = "ADAPTIVE_INSIGHTS", database = environ['SNOWPARK_DATABASE'], auto_create_table = True, overwrite = True)
    # Return statuses
    return_status = "Snowflake stage status: " + str(put_results.status) + ". " + "Snowflake table creation status: " + str(pandas_write_status.to_pandas())
    # Close Snowflake session
    conn.close()
    return return_status  # Adding a return() function so the Snowpark status will be printed in the main file and logged in DataOps.
