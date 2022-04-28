import os

from dotenv import load_dotenv

from snowflake_connector import SnowflakeConnector
import utils


def main():
    load_dotenv()  # only on local run
    # print(os.environ)

    query_file_names = os.environ["INPUT_QUERY_FILES"]
    warehouse = os.environ["INPUT_SNOWFLAKE_WAREHOUSE"]
    snowflake_account = os.environ["INPUT_SNOWFLAKE_ACCOUNT"]
    snowflake_username = os.environ["INPUT_SNOWFLAKE_USERNAME"]
    snowflake_password = os.environ["INPUT_SNOWFLAKE_PASSWORD"]
    snowflake_role = os.environ.get("INPUT_SNOWFLAKE_ROLE", "")

    sql_files = query_file_names.split(",")

    queries = []
    for sql_file in sql_files:
        with open(sql_file, "r") as f:
            sql = "".join([line.strip() for line in f.readlines()])
        queries += [n for n in sql.split(";") if n]

    with SnowflakeConnector(snowflake_account, snowflake_username, snowflake_password) as con:
        if snowflake_role:
            con.set_user_role(snowflake_role)

        con.set_db_warehouse(warehouse)

        # default, run all queries async
        for query in queries:
            result = con.query(query)
            print(f"[!] Running query ### - {query}")
            print(f"[!] Query Resule ### - {result}")

    # utils.set_github_action_output("queries_results", json.dumps(json_results))


if __name__ == "__main__":
    main()
