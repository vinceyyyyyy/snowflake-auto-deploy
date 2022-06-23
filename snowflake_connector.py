from io import StringIO
import snowflake.connector


class SnowflakeConnector:
    def __init__(self, account_name: str, username: str, password: str):
        self.account_name = account_name
        self.username = username
        self.password = password

    def __enter__(self):
        self.con = snowflake.connector.connect(
            user=self.username, password=self.password, account=self.account_name
        )
        self.cur = self.con.cursor()

        return self

    def __exit__(self, *exc):
        self.con.close()

    def set_db_warehouse(self, warehouse: str):
        return self._query(f"USE WAREHOUSE {warehouse}")

    def set_user_role(self, role: str):
        return self._query(f"USE ROLE {role}")

    def _query(self, query_str: str):
        self.cur.execute(query_str)
        return self.cur.fetchone()

    def query_sql_file(self, stream: StringIO):
        return self.con.execute_stream(stream, remove_comments=True)
