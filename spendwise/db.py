"""Database layer: connection factory + schema initialisation."""
import os
from pathlib import Path
import mysql.connector

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "spendwise"),
}

SCHEMA_FILE = Path(__file__).parent / "database" / "schema.sql"


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    """Create the database and all tables from database/schema.sql (idempotent)."""
    cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()
    for statement in SCHEMA_FILE.read_text(encoding="utf-8").split(";"):
        if statement.strip():
            cur.execute(statement)
    conn.commit()
    cur.close()
    conn.close()
    print("Database ready:", DB_CONFIG["database"])


if __name__ == "__main__":
    init_db()
