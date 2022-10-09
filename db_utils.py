import sqlite3


DB_LOCATION = "db/matches_odds"
connection = None


def get_sqlite_connection() -> sqlite3.Connection:
    """
    Singleton to return a SQLite connection or to declare it if there is none
    Returns:
        SQLite connection
    """
    global connection
    if connection is None:
        connection = sqlite3.connect(DB_LOCATION)
        connection.row_factory = sqlite3.Row
    return connection


def close_sqlite_connection():
    """
    Close SQLite connection if there is one open and initialize to None the connection variable.
    Returns:
        None
    """
    global connection
    if connection is not None:
        connection.close()
    connection = None


def select_from_sqlite(query_select, one=True):
    con = get_sqlite_connection()
    cur = con.cursor()
    cur.execute(query_select)
    if one:
        rows = cur.fetchone()
    else:
        rows = cur.fetchall()
    cur.close()
    return rows