# Postgres wrapper

import psycopg2 as db
import pandas as pd
from uuid import uuid4
from typing import List, Optional
import os
import dotenv

dotenv.load_dotenv(override=True)

username = os.environ['SQL_USERNAME']
host = os.environ['SQL_HOST']
password = os.environ['SQL_PASSWORD']
port = os.environ['port']


class SQLConnection:
    def __init__(
        self,
        dbname,
        user,
        password,
        host='dw.c1i5dspnearp.eu-west-2.rds.amazonaws.com',
        port=5432,
    ):
        self.current_cursor = str(uuid4())
        self.db_name = f''
        self.auth = dict(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )

    def q(self, query: str) -> Optional[List[str]]:
        """Executes a query and returns the result"""
        res = None
        with db.connect(**self.auth) as con:
            cur = con.cursor()
            for q in query.split(";"):
                try:
                    res = pd.read_sql_query(q.strip(), con)
                except (TypeError, ValueError):
                    pass
        return res
