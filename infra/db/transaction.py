import sqlite3

from use_cases.repositories import TransactionManager


class SqliteTransactionManager(TransactionManager):
    """Implementação concreta de TransactionManager sobre sqlite3. Os use
    cases dependem apenas da interface (use_cases.repositories.TransactionManager).
    """

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def __enter__(self) -> "SqliteTransactionManager":
        self._conn.execute("BEGIN")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is None:
            self._conn.execute("COMMIT")
        else:
            self._conn.execute("ROLLBACK")
