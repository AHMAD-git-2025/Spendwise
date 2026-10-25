"""SpendWise admin panel: read-only view of every table, schema and row.

Setup:
  1. Copy admin.py next to app.py, and admin.html into templates/
  2. In .env add:   ADMIN_PASSWORD=choose-a-strong-password
  3. In app.py, after `app = Flask(...)`, add:
         from admin import admin_bp
         app.register_blueprint(admin_bp)
  4. Open http://localhost:5000/admin

Security: pages are served no-store (Back/Forward cannot reveal them after logout),
sessions expire after 15 min idle, logout is POST-only, login is rate-limited.
"""
import os
import time
from datetime import date, datetime
from decimal import Decimal
from functools import wraps
from hmac import compare_digest

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from db import DB_CONFIG, get_db_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
IDLE_TIMEOUT = 15 * 60         # auto sign-out after 15 min of inactivity
MAX_FAILS, LOCK_SECONDS = 5, 300
_fails = {}                    # ip -> (count, locked_until)
MASKED = {"password"}          # columns never sent to the browser
ROW_LIMIT = 1000               # max rows per table


def admin_required(view):
    @wraps(view)
    def wrapper(*a, **kw):
        last = session.get("admin_at")
        if not session.get("is_admin") or not last or time.time() - last > IDLE_TIMEOUT:
            session.pop("is_admin", None)
            session.pop("admin_at", None)
            if request.path.startswith("/admin/api"):
                return jsonify(error="unauthorized"), 401
            return redirect(url_for("admin.login"))
        session["admin_at"] = time.time()      # sliding idle timeout
        return view(*a, **kw)
    return wrapper


@admin_bp.after_request
def no_cache(resp):
    """Never let the browser store admin pages, so Back/Forward can't show them after logout."""
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0, private"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


def _clean(v):
    if isinstance(v, (datetime, date)):
        return v.isoformat(sep=" ") if isinstance(v, datetime) else v.isoformat()
    if isinstance(v, Decimal):
        return str(v)
    if isinstance(v, (bytes, bytearray)):
        return v.decode("utf-8", "replace")
    return v


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    expected = os.getenv("ADMIN_PASSWORD", "")
    error = ""
    ip = request.remote_addr or "?"
    count, locked_until = _fails.get(ip, (0, 0))
    if request.method == "POST":
        if time.time() < locked_until:
            error = "Too many attempts. Try again in a few minutes."
        elif expected and compare_digest(request.form.get("password", ""), expected):
            _fails.pop(ip, None)
            session["is_admin"] = True
            session["admin_at"] = time.time()
            return redirect(url_for("admin.index"))
        else:
            count += 1
            _fails[ip] = (count, time.time() + LOCK_SECONDS if count >= MAX_FAILS else 0)
            if count >= MAX_FAILS:
                _fails[ip] = (0, time.time() + LOCK_SECONDS)
            error = "Wrong password" if expected else "Set ADMIN_PASSWORD in .env first"
    return render_template("admin_login.html", error=error)


@admin_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")


@admin_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id, email, first_name, last_name FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        # Delete dependent tables explicitly to guarantee clean deletion across all configurations
        for tbl in ["expenses", "income", "budgets", "goals", "notifications", "user_preferences"]:
            try:
                cur.execute(f"DELETE FROM `{tbl}` WHERE user_id = %s", (user_id,))
            except Exception:
                pass

        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        user_label = user.get("email") or f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or str(user_id)
        return jsonify({
            "success": True,
            "message": f"User '{user_label}' (ID: {user_id}) deleted successfully"
        }), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@admin_bp.route("/api/table/<string:table_name>/<int:row_id>", methods=["DELETE"])
@admin_required
def delete_table_row(table_name, row_id):
    if table_name == "users":
        return delete_user(row_id)

    db = DB_CONFIG["database"]
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s", (db, table_name))
        if not cur.fetchone():
            return jsonify({"success": False, "error": "Invalid table"}), 400

        cur.execute("""
            SELECT COLUMN_NAME
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_KEY='PRI'
        """, (db, table_name))
        pk_row = cur.fetchone()
        if not pk_row:
            return jsonify({"success": False, "error": "Table has no primary key"}), 400
        pk_col = pk_row["COLUMN_NAME"]

        cur.execute(f"DELETE FROM `{table_name}` WHERE `{pk_col}` = %s", (row_id,))
        conn.commit()
        return jsonify({"success": True, "message": f"Row #{row_id} deleted from {table_name}"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@admin_bp.route("/api/ping")
@admin_required
def ping():
    return jsonify(ok=True)


@admin_bp.route("/")
@admin_required
def index():
    return render_template("admin.html")


@admin_bp.route("/api/data")
@admin_required
def data():
    db = DB_CONFIG["database"]
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT TABLE_NAME AS t FROM information_schema.TABLES "
                "WHERE TABLE_SCHEMA=%s AND TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME", (db,))
    names = [r["t"] for r in cur.fetchall()]
    tables = []
    for name in names:
        cur.execute("SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY, EXTRA "
                    "FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s "
                    "ORDER BY ORDINAL_POSITION", (db, name))
        cols = [{"name": c["COLUMN_NAME"], "type": c["COLUMN_TYPE"],
                 "nullable": c["IS_NULLABLE"] == "YES", "default": _clean(c["COLUMN_DEFAULT"]),
                 "primary_key": c["COLUMN_KEY"] == "PRI", "unique": c["COLUMN_KEY"] == "UNI",
                 "auto_increment": "auto_increment" in (c["EXTRA"] or "")} for c in cur.fetchall()]
        cur.execute("SELECT k.COLUMN_NAME c, k.REFERENCED_TABLE_NAME rt, k.REFERENCED_COLUMN_NAME rc, r.DELETE_RULE dr "
                    "FROM information_schema.KEY_COLUMN_USAGE k "
                    "JOIN information_schema.REFERENTIAL_CONSTRAINTS r "
                    "ON r.CONSTRAINT_NAME=k.CONSTRAINT_NAME AND r.CONSTRAINT_SCHEMA=k.TABLE_SCHEMA "
                    "WHERE k.TABLE_SCHEMA=%s AND k.TABLE_NAME=%s AND k.REFERENCED_TABLE_NAME IS NOT NULL", (db, name))
        fks = [{"column": f["c"], "references_table": f["rt"], "references_column": f["rc"],
                "on_delete": f["dr"] if f["dr"] != "RESTRICT" else None} for f in cur.fetchall()]
        cur.execute(f"SELECT COUNT(*) AS n FROM `{name}`")
        total = cur.fetchone()["n"]
        cur.execute(f"SELECT * FROM `{name}` LIMIT {ROW_LIMIT}")
        rows = [{k: (None if v is None else "••••" if k in MASKED else _clean(v)) for k, v in r.items()}
                for r in cur.fetchall()]
        pk = next((c["name"] for c in cols if c["primary_key"]), None)
        tables.append({"name": name, "primary_key": pk, "columns": cols, "foreign_keys": fks,
                       "row_count": total, "rows": rows})
    cur.close(); conn.close()
    return jsonify(database=db, engine="MySQL / MariaDB", tables=tables)
