"""Database layer: connection factory + schema initialisation.
Supports both local MySQL/MariaDB and managed cloud providers (e.g., Aiven MySQL).
"""
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import mysql.connector

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SCHEMA_FILE = Path(__file__).parent / "database" / "schema.sql"


def get_db_config():
    """
    Builds the MySQL configuration dictionary from environment variables.
    Supports individual parameters (DB_HOST, DB_USER, etc.) or full connection URIs
    (DATABASE_URL, MYSQL_URL, AIVEN_MYSQL_URL).
    """
    conn_url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL") or os.getenv("AIVEN_MYSQL_URL")

    if conn_url:
        parsed = urlparse(conn_url)
        params = parse_qs(parsed.query)
        cfg = {
            "host": parsed.hostname or "localhost",
            "port": parsed.port or 3306,
            "user": parsed.username or "root",
            "password": parsed.password or "",
            "database": (parsed.path or "").lstrip("/") or "spendwise",
        }
        ssl_mode = params.get("ssl-mode", [""])[0].lower()
        if ssl_mode in ("required", "verify-ca", "verify-identity") or "aivencloud.com" in cfg["host"]:
            cfg["ssl_disabled"] = False
        return cfg

    cfg = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "spendwise"),
    }

    if os.getenv("DB_SSL", "").lower() in ("1", "true", "required") or "aivencloud.com" in cfg["host"]:
        cfg["ssl_disabled"] = False

    ca_path = os.getenv("DB_SSL_CA")
    if ca_path and os.path.exists(ca_path):
        cfg["ssl_ca"] = ca_path

    return cfg


DB_CONFIG = get_db_config()


def get_db_connection():
    """Returns a fresh connection to the configured MySQL database."""
    return mysql.connector.connect(**get_db_config())


def init_db():
    """
    Create tables from database/schema.sql (idempotent).
    Works on both local servers and managed cloud databases (like Aiven) where
    the database name is pre-assigned (e.g., 'defaultdb') and CREATE DATABASE is restricted.
    """
    cfg = get_db_config()
    target_db = cfg.get("database") or "spendwise"

    conn = None
    connected_to_db = False

    # 1. First, try connecting directly to the target database (recommended for Aiven/cloud)
    try:
        conn = mysql.connector.connect(**cfg)
        connected_to_db = True
    except mysql.connector.Error as err:
        # If database doesn't exist (e.g., on local MySQL), connect without database to create it
        if err.errno in (1049, 1045) and cfg.get("host") in ("localhost", "127.0.0.1"):
            no_db_cfg = {k: v for k, v in cfg.items() if k != "database"}
            conn = mysql.connector.connect(**no_db_cfg)
        else:
            raise

    cur = conn.cursor()
    schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")

    for raw_stmt in schema_sql.split(";"):
        stmt = raw_stmt.strip()
        if not stmt:
            continue

        upper_stmt = stmt.upper()

        # If already connected to target database (e.g. Aiven defaultdb), skip CREATE DATABASE and USE statements
        if connected_to_db:
            if upper_stmt.startswith("CREATE DATABASE") or upper_stmt.startswith("USE "):
                continue

        try:
            cur.execute(stmt)
        except mysql.connector.Error as exc:
            # Ignore warning if table or database already exists
            if exc.errno in (1007, 1050):
                continue
            # If CREATE DATABASE fails on cloud host with restricted permissions, ignore and proceed
            if "CREATE DATABASE" in upper_stmt and exc.errno == 1044:
                continue
            raise

    conn.commit()
    cur.close()
    conn.close()
    print("Database ready:", target_db)


if __name__ == "__main__":
    init_db()
