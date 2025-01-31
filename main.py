import os

from dotenv import load_dotenv

from snowflake_connector import SnowflakeConnector


def main():
    load_dotenv()  # only on local run
    # print(os.environ)

    query_file_names = os.environ["INPUT_QUERY_FILES"]
    warehouse = os.environ["INPUT_SNOWFLAKE_WAREHOUSE"]
    snowflake_account = os.environ["INPUT_SNOWFLAKE_ACCOUNT"]
    snowflake_username = os.environ["INPUT_SNOWFLAKE_USERNAME"]
    snowflake_password = os.environ["INPUT_SNOWFLAKE_PASSWORD"]
    snowflake_database = os.environ.get("INPUT_SNOWFLAKE_DATABASE", "")
    snowflake_schema = os.environ.get("INPUT_SNOWFLAKE_SCHEMA", "")
    snowflake_role = os.environ.get("INPUT_SNOWFLAKE_ROLE", "")

    sql_files = [f for f in query_file_names.split("\n") if f]

    with SnowflakeConnector(snowflake_account, snowflake_username, snowflake_password) as con:
        if snowflake_role:
            con.set_user_role(snowflake_role)
        if snowflake_database:
            con.set_database(snowflake_database)
        if snowflake_schema:
            con.set_schema(snowflake_schema)

        con.set_db_warehouse(warehouse)

        # default, run all queries async
        for sql_file in sql_files:
            print(f"Running query file ### - {sql_file}")
            with open(sql_file, "r") as f:
                results = con.query_sql_file(f)
                for cur in results:
                    for row in cur:
                        print(f"[!] Query Result ### - {row}")

# utils.set_github_action_output("queries_results", json.dumps(json_results))


if __name__ == "__main__":
    main()
