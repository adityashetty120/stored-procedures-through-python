import os
import pymysql
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class DbConfig:
    def __init__(self, server, port, db_name, user, pswd):
        self.server = server
        self.port = port
        self.db_name = db_name
        self.user = user
        self.pswd = pswd

    def print_details(self):
        print("Using db connection: host: %s:%d, db: %s" % (self.server, self.port, self.db_name))


def _load_config_from_env() -> DbConfig:
    """
    Reads DB connection settings from environment variables.

    Required environment variables:
        DB_HOST     - MySQL server hostname
        DB_PORT     - MySQL server port (integer)
        DB_NAME     - Database name
        DB_USER     - MySQL username
        DB_PASSWORD - MySQL password
    """
    missing = [v for v in ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD") if not os.environ.get(v)]
    if missing:
        raise EnvironmentError(
            "Missing required environment variable(s): {}. "
            "Set them before calling run_proc().".format(", ".join(missing))
        )
    return DbConfig(
        server=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        db_name=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        pswd=os.environ["DB_PASSWORD"],
    )


def _get_connection(config: DbConfig):
    config.print_details()
    return pymysql.connect(
        host=config.server,
        user=config.user,
        passwd=config.pswd,
        db=config.db_name,
        port=config.port,
        use_unicode=True,
        charset="utf8mb4",
    )


def call_proc(proc_name: str, registry_table: str = "proc_query_registry") -> pd.DataFrame:
    """
    Looks up the SQL query registered under `proc_name` in `registry_table`,
    executes it, and returns the result as a pandas DataFrame.

    Connection settings are read from environment variables:
        DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

    Parameters
    ----------
    proc_name : str
        The name of the procedure/query entry to look up.
    registry_table : str, optional
        Name of the table that holds (proc_name, query) rows.
        Defaults to "proc_query_registry".

    Returns
    -------
    pd.DataFrame
        Query results as a DataFrame.

    Raises
    ------
    EnvironmentError
        If any required environment variable is missing.
    ValueError
        If no entry is found for the given proc_name.
    """
    config = _load_config_from_env()
    conn = None
    try:
        conn = _get_connection(config)

        lookup_query = "SELECT `query` FROM {} WHERE proc_name = %s LIMIT 1".format(registry_table)
        lookup_df = pd.read_sql(lookup_query, conn, params=(proc_name,))

        if lookup_df.empty:
            raise ValueError("No query found for proc_name: '{}'".format(proc_name))

        sql_query = lookup_df.iloc[0]["query"]
        print("Executing query for proc_name '{}': {}".format(proc_name, sql_query))

        return pd.read_sql(sql_query, conn)

    finally:
        if conn:
            conn.close()
