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
        return self.query(f"USE WAREHOUSE {warehouse}")

    def set_user_role(self, role: str):
        return self.query(f"USE ROLE {role}")

    def query(self, query_str: str):
        self.cur.execute(query_str)
        return self.cur.fetchone()
