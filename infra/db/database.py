import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent.parent / "database" / "schema.sql"


def get_connection(db_path: str) -> sqlite3.Connection:
    """Abre (e cria, se necessário) a conexão SQLite usada por toda a aplicação.
    isolation_level=None desliga o autocommit implícito do driver, deixando o
    controle de transações explícito para o SqliteTransactionManager.
    """
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def get_test_connection() -> sqlite3.Connection:
    """Conexão SQLite em memória, usada nos testes de integração leve."""
    conn = sqlite3.connect(":memory:", isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    init_db(conn)
    return conn
