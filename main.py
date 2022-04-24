import os
import json

from dotenv import load_dotenv

from snowflake_connector import SnowflakeConnector
import utils


def main():
    load_dotenv()  # only on local run
    print(os.environ)

    query_file_name = os.environ["INPUT_QUERY_FILE"]
    warehouse = os.environ["INPUT_SNOWFLAKE_WAREHOUSE"]
    snowflake_account = os.environ["INPUT_SNOWFLAKE_ACCOUNT"]
    snowflake_username = os.environ["INPUT_SNOWFLAKE_USERNAME"]
    snowflake_password = os.environ["INPUT_SNOWFLAKE_PASSWORD"]
    snowflake_role = os.environ.get("INPUT_SNOWFLAKE_ROLE", "")

    with open(query_file_name, "r") as f:
        sql = "".join(f.readlines())
    queries = [n for n in sql.split(";") if n]

    with SnowflakeConnector(snowflake_account, snowflake_username, snowflake_password) as con:
        if snowflake_role:
            con.set_user_role(snowflake_role)

        con.set_db_warehouse(warehouse)

        # default, run all queries async
        json_results = {}
        for query in queries:
            query_result = con.query(query)
            print("### Running query ###")
            print(f"[!] Query id - {query_result.query_id}")
            print(f"[!] Running query ### - {query}")
            json_results[query_result.query_id] = query_result.fetch_results_sync()

    utils.set_github_action_output("queries_results", json.dumps(json_results))


if __name__ == "__main__":
    main()
