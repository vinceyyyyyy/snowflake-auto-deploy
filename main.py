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
    snowflake_role = os.environ.get("INPUT_SNOWFLAKE_ROLE", "")

    sql_files = query_file_names.split(r"\n")

    with SnowflakeConnector(snowflake_account, snowflake_username, snowflake_password) as con:
        if snowflake_role:
            con.set_user_role(snowflake_role)

        con.set_db_warehouse(warehouse)

        # default, run all queries async
        for sql_file in sql_files:
            with open(sql_file, "r") as f:
                results = con.query_sql_file(f)
                for cur in results:
                    for row in cur:
                        print(f"[!] Query Resule ### - {row}")

    # utils.set_github_action_output("queries_results", json.dumps(json_results))


if __name__ == "__main__":
    main()
