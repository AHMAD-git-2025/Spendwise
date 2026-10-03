from functools import wraps
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
import os
import traceback
from db import get_db_connection, init_db
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")  # set SECRET_KEY in .env
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

# ============================================================
# 60 DAY DATA RETENTION
# ============================================================

TRIAL_DAYS = 60


# ============================================================
# CHECK 60 DAY PERIOD
# ============================================================

def check_60_day_period(user_id):

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT created_at, data_deleted_at
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            return None

        # Data has already been deleted
        if user["data_deleted_at"] is not None:

            return {
                "expired": True,
                "days_remaining": 0
            }

        created_at = user["created_at"]

        # 60 days from account creation
        expiry_date = created_at + timedelta(days=TRIAL_DAYS)

        now = datetime.now()

        # ----------------------------------------------------
        # 60 DAYS HAVE PASSED
        # ----------------------------------------------------

        if now >= expiry_date:

            # Delete income
            cursor.execute("""
                DELETE FROM income
                WHERE user_id = %s
            """, (user_id,))

            # Delete expenses
            cursor.execute("""
                DELETE FROM expenses
                WHERE user_id = %s
            """, (user_id,))

            # Delete budgets
            cursor.execute("""
                DELETE FROM budgets
                WHERE user_id = %s
            """, (user_id,))

            # Delete goals
            cursor.execute("""
                DELETE FROM goals
                WHERE user_id = %s
            """, (user_id,))

            cursor.execute("DELETE FROM notifications WHERE user_id = %s", (user_id,))

            # Remember that deletion has happened
            cursor.execute("""
                UPDATE users
                SET data_deleted_at = NOW()
                WHERE id = %s
            """, (user_id,))

            conn.commit()

            return {
                "expired": True,
                "days_remaining": 0
            }

        # ----------------------------------------------------
        # STILL WITHIN 60 DAYS
        # ----------------------------------------------------

        seconds_remaining = (
            expiry_date - now
        ).total_seconds()

        days_remaining = int(
            (seconds_remaining + 86399) // 86400
        )

        return {
            "expired": False,
            "days_remaining": days_remaining,
            "expiry_date": expiry_date.isoformat()
        }

    except Exception as e:

        if conn:
            conn.rollback()

        print("60 day check error:", e)

        return None

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# ---------------------------------------------------------------------------
# Auth helper
#
# Wrap any page route that should only be visible to logged-in users with
# @login_required. It sends anyone without a session straight to /login,
# and remembers where they were headed via ?next=... so you can send them
# back after they log in (the login.html below already reads this).
#
# Use it on every new dashboard-style page you add:
#
#   @app.route("/expenses")
#   @login_required
#   def expenses_page():
#       return render_template("expenses.html")
#
# ---------------------------------------------------------------------------

def wants_json():
    """Determine whether the client expects a JSON response (API/AJAX) or HTML."""
    return (
        request.path.startswith("/api/")
        or request.is_json
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
    )


def login_required(view_func):

    @wraps(view_func)
    def wrapped(*args, **kwargs):

        if "user_id" not in session:
            if wants_json():
                return jsonify({
                    "success": False,
                    "error": "Unauthorized",
                    "message": "You must be logged in to perform this action.",
                    "status_code": 401
                }), 401

            return redirect(
                url_for(
                    "login_page",
                    next=request.path
                )
            )

        # Check the 60-day period
        result = check_60_day_period(
            session["user_id"]
        )

        # User no longer exists
        if result is None:
            session.clear()
            if wants_json():
                return jsonify({
                    "success": False,
                    "error": "Unauthorized",
                    "message": "User session expired or user no longer exists.",
                    "status_code": 401
                }), 401

            return redirect(
                url_for("login_page")
            )

        # If 60 days have passed,
        # still allow the user to access the website.
        #
        # Their financial data has already been deleted.
        #
        # We are NOT blocking the account.

        return view_func(*args, **kwargs)

    return wrapped


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------



@app.route("/")
def home():
    return render_template("homepage.html")


# Registration page
@app.route("/register")
def register_page():
    if "user_id" in session:
        return redirect(url_for("dashboard_page"))
    return render_template("register.html")


# Login Page
@app.route("/login")
def login_page():
    if "user_id" in session:
        return redirect(url_for("dashboard_page"))
    return render_template("login.html")


# ============================================================
# PUBLIC INFORMATION PAGES
# ============================================================

@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/how-it-works")
def how_it_works_page():
    return render_template("how-it-works.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


# Income page
@app.route("/income")
@login_required
def income_page():
    return render_template("income.html")


# Expenses page
@app.route("/expenses")
@login_required
def expenses_page():
    return render_template("expenses.html")

# ============================================================
# 60 DAY COUNTDOWN API
# ============================================================

@app.route("/api/trial", methods=["GET"])
@login_required
def trial_api():

    user_id = session["user_id"]

    result = check_60_day_period(user_id)

    if result is None:

        return jsonify({
            "success": False,
            "message": "Unable to check account period"
        }), 500

    return jsonify({
        "success": True,
        "expired": result["expired"],
        "days_remaining": result["days_remaining"],
        "expiry_date": result.get("expiry_date")
    })




# ---------------------------------------------------------------------------
# Add future pages here, following the same pattern:
#
# @app.route("/budget")
# @login_required
# def budget_page():
#     return render_template("budget.html")
#
# @app.route("/reports")
# @login_required
# def reports_page():
#     return render_template("reports.html")
#
# @app.route("/goals")
# @login_required
# def goals_page():
#     return render_template("goals.html")
#
# @app.route("/settings")
# @login_required
# def settings_page():
#     return render_template("settings.html")
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Registration API
# ---------------------------------------------------------------------------

@app.route("/api/register", methods=["POST"])
def register_user():

    data = request.get_json()

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    # Check that all fields are provided
    if not first_name or not last_name or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT id FROM users WHERE email = %s",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()

        return jsonify({
            "success": False,
            "message": "Email already registered"
        }), 409

    # Hash password
    hashed_password = generate_password_hash(password)

    # Insert user
    sql = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES (%s, %s, %s, %s)
    """

    values = (
        first_name,
        last_name,
        email,
        hashed_password
    )

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Account created successfully"
    }), 201

# ============================================================
# DASHBOARD PAGE
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard.html")


# ============================================================
# DASHBOARD API
# ============================================================

@app.route("/api/dashboard", methods=["GET"])
@login_required
def dashboard_api():

    user_id = session["user_id"]
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ----------------------------------------------------
        # USER
        # ----------------------------------------------------
        cursor.execute("""
            SELECT id, first_name, last_name, email
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        # ----------------------------------------------------
        # TOTAL INCOME
        # ----------------------------------------------------
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM income
            WHERE user_id = %s
        """, (user_id,))

        total_income = float(cursor.fetchone()["total"] or 0)

        # ----------------------------------------------------
        # TOTAL EXPENSES
        # ----------------------------------------------------
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = %s
        """, (user_id,))

        total_expenses = float(cursor.fetchone()["total"] or 0)

        # ----------------------------------------------------
        # BALANCE
        # ----------------------------------------------------
        balance = total_income - total_expenses

        # ----------------------------------------------------
        # CURRENT MONTH
        # ----------------------------------------------------
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM income
            WHERE user_id = %s
              AND YEAR(income_date) = YEAR(CURDATE())
              AND MONTH(income_date) = MONTH(CURDATE())
        """, (user_id,))

        monthly_income = float(cursor.fetchone()["total"] or 0)

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = %s
              AND YEAR(expense_date) = YEAR(CURDATE())
              AND MONTH(expense_date) = MONTH(CURDATE())
        """, (user_id,))

        monthly_expenses = float(cursor.fetchone()["total"] or 0)

        # ----------------------------------------------------
        # EXPENSE BY CATEGORY
        # ----------------------------------------------------
        cursor.execute("""
            SELECT
                category,
                COALESCE(SUM(amount), 0) AS amount
            FROM expenses
            WHERE user_id = %s
            GROUP BY category
            ORDER BY amount DESC
        """, (user_id,))

        category_rows = cursor.fetchall()

        category_expenses = [
            {
                "category": row["category"],
                "amount": float(row["amount"] or 0)
            }
            for row in category_rows
        ]

        # ----------------------------------------------------
        # LAST 6 MONTHS
        # ----------------------------------------------------
        cursor.execute("""
            SELECT
                DATE_FORMAT(income_date, '%Y-%m') AS month,
                COALESCE(SUM(amount), 0) AS amount
            FROM income
            WHERE user_id = %s
              AND income_date >= DATE_SUB(CURDATE(), INTERVAL 5 MONTH)
            GROUP BY DATE_FORMAT(income_date, '%Y-%m')
            ORDER BY month
        """, (user_id,))

        income_months = cursor.fetchall()

        cursor.execute("""
            SELECT
                DATE_FORMAT(expense_date, '%Y-%m') AS month,
                COALESCE(SUM(amount), 0) AS amount
            FROM expenses
            WHERE user_id = %s
              AND expense_date >= DATE_SUB(CURDATE(), INTERVAL 5 MONTH)
            GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
            ORDER BY month
        """, (user_id,))

        expense_months = cursor.fetchall()

        monthly_data = {}

        for row in income_months:
            monthly_data[row["month"]] = {
                "income": float(row["amount"] or 0),
                "expense": 0
            }

        for row in expense_months:
            if row["month"] not in monthly_data:
                monthly_data[row["month"]] = {
                    "income": 0,
                    "expense": 0
                }

            monthly_data[row["month"]]["expense"] = float(
                row["amount"] or 0
            )

        monthly_trend = []

        for month in sorted(monthly_data.keys()):
            monthly_trend.append({
                "month": month,
                "income": monthly_data[month]["income"],
                "expense": monthly_data[month]["expense"]
            })

        # ----------------------------------------------------
        # RECENT TRANSACTIONS
        # ----------------------------------------------------
        cursor.execute("""
            SELECT
                id,
                source AS name,
                category,
                amount,
                income_date AS transaction_date,
                'income' AS transaction_type
            FROM income
            WHERE user_id = %s

            UNION ALL

            SELECT
                id,
                description AS name,
                category,
                amount,
                expense_date AS transaction_date,
                'expense' AS transaction_type
            FROM expenses
            WHERE user_id = %s

            ORDER BY transaction_date DESC
            LIMIT 6
        """, (user_id, user_id))

        recent_rows = cursor.fetchall()

        recent_transactions = []

        for row in recent_rows:
            recent_transactions.append({
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "amount": float(row["amount"] or 0),
                "date": row["transaction_date"].strftime("%Y-%m-%d")
                if row["transaction_date"] else None,
                "type": row["transaction_type"]
            })

        # ----------------------------------------------------
        # BUDGETS & SPENDING
        # ----------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM budgets
            WHERE user_id = %s
        """, (user_id,))
        budget_count = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT id, category, amount, period, budget_month
            FROM budgets
            WHERE user_id = %s
            ORDER BY budget_month DESC, id DESC
            LIMIT 5
        """, (user_id,))
        budget_rows = cursor.fetchall()

        budget_items = []
        for b_row in budget_rows:
            cat = b_row["category"]
            b_amt = float(b_row["amount"] or 0)
            b_month = b_row["budget_month"]
            if hasattr(b_month, "year"):
                y, m = b_month.year, b_month.month
            else:
                y = int(str(b_month)[:4])
                m = int(str(b_month)[5:7])

            if cat == "Overall":
                cursor.execute("""
                    SELECT COALESCE(SUM(amount), 0) AS spent
                    FROM expenses
                    WHERE user_id = %s
                      AND YEAR(expense_date) = %s
                      AND MONTH(expense_date) = %s
                """, (user_id, y, m))
            else:
                cursor.execute("""
                    SELECT COALESCE(SUM(amount), 0) AS spent
                    FROM expenses
                    WHERE user_id = %s
                      AND category = %s
                      AND YEAR(expense_date) = %s
                      AND MONTH(expense_date) = %s
                """, (user_id, cat, y, m))
            b_spent = float(cursor.fetchone()["spent"] or 0)

            budget_items.append({
                "id": b_row["id"],
                "category": cat,
                "spent": b_spent,
                "limit": b_amt,
                "period": b_row["period"]
            })

        # ----------------------------------------------------
        # GOALS
        # ----------------------------------------------------
        cursor.execute("""
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(target_amount), 0) AS target,
                COALESCE(SUM(saved_amount), 0) AS saved
            FROM goals
            WHERE user_id = %s
        """, (user_id,))

        goal_data = cursor.fetchone()

        cursor.execute("""
            SELECT id, name, target_amount, saved_amount, deadline, category, icon
            FROM goals
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 5
        """, (user_id,))
        goal_rows = cursor.fetchall()

        goal_items = [
            {
                "id": g["id"],
                "name": g["name"],
                "saved": float(g["saved_amount"] or 0),
                "target": float(g["target_amount"] or 0),
                "category": g["category"],
                "icon": g.get("icon", "🎯"),
                "deadline": g["deadline"].isoformat() if g.get("deadline") and hasattr(g["deadline"], "isoformat") else (str(g["deadline"]) if g.get("deadline") else None)
            }
            for g in goal_rows
        ]

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------
        return jsonify({
            "success": True,

            "user": {
                "id": user["id"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "email": user["email"]
            },

            "summary": {
                "balance": balance,
                "total_income": total_income,
                "total_expenses": total_expenses,
                "monthly_income": monthly_income,
                "monthly_expenses": monthly_expenses
            },

            "category_expenses": category_expenses,

            "monthly_trend": monthly_trend,

            "recent_transactions": recent_transactions,

            "budgets": {
                "count": budget_count,
                "items": budget_items
            },

            "goals": {
                "count": goal_data["total"],
                "target": float(goal_data["target"] or 0),
                "saved": float(goal_data["saved"] or 0),
                "items": goal_items
            },

            "goal_items": goal_items
        })

    except Exception as e:

        print("Dashboard API Error:", e)

        return jsonify({
            "success": False,
            "message": "Unable to load dashboard data"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# Login API
# ---------------------------------------------------------------------------

@app.route("/api/login", methods=["POST"])
def login_user():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, first_name, last_name, email, password FROM users WHERE email = %s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user or not check_password_hash(user["password"], password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    session["user_id"] = user["id"]

    return jsonify({
        "success": True,
        "message": "Logged in successfully",
        "user": {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"]
        }
    }), 200


@app.route("/api/logout", methods=["POST"])
def logout_user():
    session.pop("user_id", None)
    return jsonify({"success": True, "message": "Logged out"}), 200


# Lets any page (current or future) check who's logged in, e.g. on load to
# populate the avatar/name in the topbar, or to decide whether to show
# logged-in vs logged-out nav links.
@app.route("/api/me", methods=["GET"])
def get_current_user():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, first_name, last_name, email FROM users WHERE id = %s",
        (session["user_id"],)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        session.pop("user_id", None)
        return jsonify({"success": False, "message": "Not logged in"}), 401

    return jsonify({"success": True, "user": user}), 200


# ---------------------------------------------------------------------------
# Income API
# ---------------------------------------------------------------------------

ALLOWED_CATEGORIES = {
    "Salary", "Freelance", "Business", "Investment",
    "Interest", "Rental Income", "Gift", "Bonus", "Other"
}

ALLOWED_FREQUENCIES = {"Monthly", "Weekly", "Yearly"}


@app.route("/api/income", methods=["GET"])
def get_income():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "You must be logged in to view income"
        }), 401

    user_id = session["user_id"]

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, source, amount, category, income_date, account,
               recurring, frequency, notes, created_at
        FROM income
        WHERE user_id = %s
        ORDER BY income_date DESC, id DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # Convert non-JSON-safe types (Decimal, date) to plain values
    income = []
    for row in rows:
        income.append({
            "id": row["id"],
            "source": row["source"],
            "amount": float(row["amount"]),
            "category": row["category"],
            "income_date": row["income_date"].isoformat() if row["income_date"] else None,
            "account": row["account"],
            "recurring": bool(row["recurring"]),
            "frequency": row["frequency"],
            "notes": row["notes"],
            "created_at": row["created_at"].isoformat() if row["created_at"] else None
        })

    return jsonify({
        "success": True,
        "income": income
    }), 200


@app.route("/api/income", methods=["POST"])
def add_income():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "You must be logged in to add income"
        }), 401

    user_id = session["user_id"]
    data = request.get_json()

    source = (data.get("source") or "").strip()
    amount = data.get("amount")
    category = data.get("category")
    income_date = data.get("income_date")
    account = data.get("account") or "Bank Account"
    recurring = bool(data.get("recurring"))
    frequency = data.get("frequency")
    notes = (data.get("notes") or "").strip()

    # Required fields
    if not source or amount is None or not category or not income_date:
        return jsonify({
            "success": False,
            "message": "Source, amount, category and date are required"
        }), 400

    # Amount validation
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Amount must be a number"
        }), 400

    if amount <= 0:
        return jsonify({
            "success": False,
            "message": "Amount must be greater than zero"
        }), 400

    # Category validation
    if category not in ALLOWED_CATEGORIES:
        return jsonify({
            "success": False,
            "message": "Invalid category"
        }), 400

    # Recurring / frequency validation
    if recurring:
        if frequency not in ALLOWED_FREQUENCIES:
            return jsonify({
                "success": False,
                "message": "Invalid recurring frequency"
            }), 400
    else:
        frequency = None

    connection = get_db_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO income
        (user_id, source, amount, category, income_date, account, recurring, frequency, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        source,
        amount,
        category,
        income_date,
        account,
        recurring,
        frequency,
        notes
    )

    cursor.execute(sql, values)
    connection.commit()

    new_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Income added successfully",
        "id": new_id
    }), 201


@app.route("/api/income/<int:income_id>", methods=["DELETE"])
def delete_income(income_id):

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "You must be logged in to delete income"
        }), 401

    user_id = session["user_id"]

    connection = get_db_connection()
    cursor = connection.cursor()

    # Only delete if it belongs to the logged-in user
    cursor.execute(
        "DELETE FROM income WHERE id = %s AND user_id = %s",
        (income_id, user_id)
    )
    connection.commit()

    deleted = cursor.rowcount > 0

    cursor.close()
    connection.close()

    if not deleted:
        return jsonify({
            "success": False,
            "message": "Income entry not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Income entry deleted"
    }), 200


@app.route("/api/income/<int:income_id>", methods=["PUT"])
def update_income(income_id):

    if "user_id" not in session:
        return jsonify({"success": False, "message": "You must be logged in to update income"}), 401

    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}

    source = (data.get("source") or "").strip()
    amount = data.get("amount")
    category = data.get("category")
    income_date = data.get("income_date")
    account = data.get("account") or "Bank Account"
    recurring = bool(data.get("recurring"))
    frequency = data.get("frequency")
    notes = (data.get("notes") or "").strip()

    if not source or amount is None or not category or not income_date:
        return jsonify({"success": False, "message": "Source, amount, category and date are required"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Amount must be a number"}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than zero"}), 400

    if category not in ALLOWED_CATEGORIES:
        return jsonify({"success": False, "message": "Invalid category"}), 400

    if recurring:
        if frequency not in ALLOWED_FREQUENCIES:
            return jsonify({"success": False, "message": "Invalid recurring frequency"}), 400
    else:
        frequency = None

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE income
        SET source = %s, amount = %s, category = %s, income_date = %s,
            account = %s, recurring = %s, frequency = %s, notes = %s
        WHERE id = %s AND user_id = %s
        """,
        (source, amount, category, income_date, account,
         recurring, frequency, notes, income_id, user_id)
    )
    connection.commit()

    # rowcount is 0 when values are unchanged, so check existence instead
    cursor.execute("SELECT id FROM income WHERE id = %s AND user_id = %s", (income_id, user_id))
    exists = cursor.fetchone() is not None

    cursor.close()
    connection.close()

    if not exists:
        return jsonify({"success": False, "message": "Income entry not found"}), 404

    return jsonify({"success": True, "message": "Income updated successfully"}), 200



# ---------------------------------------------------------------------------
# Expenses API
# ---------------------------------------------------------------------------

EXPENSE_CATEGORIES = {
    "Food", "Transport", "Shopping", "Bills", "Entertainment",
    "Health", "Education", "Travel", "Rent", "Other"
}

EXPENSE_FREQUENCIES = {"Daily", "Weekly", "Monthly", "Yearly"}


@app.route("/api/expenses", methods=["GET"])
def get_expenses():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "You must be logged in to view expenses"
        }), 401

    user_id = session["user_id"]

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, description, amount, category, expense_date, payment_method,
               recurring, frequency, notes, created_at
        FROM expenses
        WHERE user_id = %s
        ORDER BY expense_date DESC, id DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # Convert non-JSON-safe types (Decimal, date) to plain values
    expenses = []
    for row in rows:
        expenses.append({
            "id": row["id"],
            "description": row["description"],
            "amount": float(row["amount"]),
            "category": row["category"],
            "expense_date": row["expense_date"].isoformat() if row["expense_date"] else None,
            "payment_method": row["payment_method"],
            "recurring": bool(row["recurring"]),
            "frequency": row["frequency"],
            "notes": row["notes"],
            "created_at": row["created_at"].isoformat() if row["created_at"] else None
        })

    return jsonify({
        "success": True,
        "expenses": expenses
    }), 200


@app.route("/api/expenses", methods=["POST"])
def add_expense():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "You must be logged in to add an expense"
        }), 401

    user_id = session["user_id"]
    data = request.get_json()

    description = (data.get("description") or "").strip()
    amount = data.get("amount")
    category = data.get("category")
    expense_date = data.get("expense_date")
    payment_method = data.get("payment_method") or "Other"
    recurring = bool(data.get("recurring"))
    frequency = data.get("frequency") or None
    notes = (data.get("notes") or "").strip()

    # Required fields
    if not description or amount is None or not category or not expense_date:
        return jsonify({
            "success": False,
            "message": "Description, amount, category and date are required"
        }), 400

    # Amount validation
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Amount must be a number"
        }), 400

    if amount <= 0:
        return jsonify({
            "success": False,
            "message": "Amount must be greater than zero"
        }), 400

    # Category validation
    if category not in EXPENSE_CATEGORIES:
        return jsonify({
            "success": False,
            "message": "Invalid category"
        }), 400

    # Recurring / frequency validation
    if recurring:
        if frequency not in EXPENSE_FREQUENCIES:
            return jsonify({
                "success": False,
                "message": "Invalid recurring frequency"
            }), 400
    else:
        frequency = None

    connection = get_db_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO expenses
        (user_id, description, amount, category, expense_date, payment_method, recurring, frequency, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        description,
        amount,
        category,
        expense_date,
        payment_method,
        recurring,
        frequency,
        notes
    )

    cursor.execute(sql, values)
    connection.commit()

    new_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Expense added successfully",
        "id": new_id
    }), 201


@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "You must be logged in to delete an expense"
        }), 401

    user_id = session["user_id"]

    connection = get_db_connection()
    cursor = connection.cursor()

    # Only delete if it belongs to the logged-in user
    cursor.execute(
        "DELETE FROM expenses WHERE id = %s AND user_id = %s",
        (expense_id, user_id)
    )
    connection.commit()

    deleted = cursor.rowcount > 0

    cursor.close()
    connection.close()

    if not deleted:
        return jsonify({
            "success": False,
            "message": "Expense entry not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Expense entry deleted"
    }), 200


@app.route("/api/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):

    if "user_id" not in session:
        return jsonify({"success": False, "message": "You must be logged in to update an expense"}), 401

    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}

    description = (data.get("description") or "").strip()
    amount = data.get("amount")
    category = data.get("category")
    expense_date = data.get("expense_date")
    payment_method = data.get("payment_method") or "Other"
    recurring = bool(data.get("recurring"))
    frequency = data.get("frequency") or None
    notes = (data.get("notes") or "").strip()

    if not description or amount is None or not category or not expense_date:
        return jsonify({"success": False, "message": "Description, amount, category and date are required"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Amount must be a number"}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than zero"}), 400

    if category not in EXPENSE_CATEGORIES:
        return jsonify({"success": False, "message": "Invalid category"}), 400

    if recurring:
        if frequency not in EXPENSE_FREQUENCIES:
            return jsonify({"success": False, "message": "Invalid recurring frequency"}), 400
    else:
        frequency = None

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET description = %s, amount = %s, category = %s, expense_date = %s,
            payment_method = %s, recurring = %s, frequency = %s, notes = %s
        WHERE id = %s AND user_id = %s
        """,
        (description, amount, category, expense_date, payment_method,
         recurring, frequency, notes, expense_id, user_id)
    )
    connection.commit()

    # rowcount is 0 when values are unchanged, so check existence instead
    cursor.execute("SELECT id FROM expenses WHERE id = %s AND user_id = %s", (expense_id, user_id))
    exists = cursor.fetchone() is not None

    cursor.close()
    connection.close()

    if not exists:
        return jsonify({"success": False, "message": "Expense entry not found"}), 404

    return jsonify({"success": True, "message": "Expense updated successfully"}), 200


# ============================================================
# BUDGET PAGE
# ============================================================

@app.route("/budget")
@login_required
def budget_page():
    return render_template("budget.html")


# ============================================================
# BUDGET API
# ============================================================

@app.route("/api/budgets", methods=["GET"])
@login_required
def get_budgets():

    user_id = session["user_id"]

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get all budgets belonging to the logged-in user
        cursor.execute("""
            SELECT
                id,
                category,
                amount,
                period,
                budget_month,
                created_at
            FROM budgets
            WHERE user_id = %s
            ORDER BY budget_month DESC, id DESC
        """, (user_id,))

        budgets = cursor.fetchall()

        # Calculate spending for every budget
        for budget in budgets:

            category = budget["category"]
            period = budget["period"]
            budget_month = budget["budget_month"]

            # Convert DATE to Python date if necessary
            if hasattr(budget_month, "year"):
                year = budget_month.year
                month = budget_month.month
            else:
                year = int(str(budget_month)[:4])
                month = int(str(budget_month)[5:7])

            # ------------------------------------------------
            # MONTHLY BUDGET
            # ------------------------------------------------
            if period == "Monthly":

                if category == "Overall":

                    cursor.execute("""
                        SELECT COALESCE(SUM(amount), 0) AS spent
                        FROM expenses
                        WHERE user_id = %s
                          AND YEAR(expense_date) = %s
                          AND MONTH(expense_date) = %s
                    """, (user_id, year, month))

                else:

                    cursor.execute("""
                        SELECT COALESCE(SUM(amount), 0) AS spent
                        FROM expenses
                        WHERE user_id = %s
                          AND category = %s
                          AND YEAR(expense_date) = %s
                          AND MONTH(expense_date) = %s
                    """, (user_id, category, year, month))

            # ------------------------------------------------
            # YEARLY BUDGET
            # ------------------------------------------------
            elif period == "Yearly":

                if category == "Overall":

                    cursor.execute("""
                        SELECT COALESCE(SUM(amount), 0) AS spent
                        FROM expenses
                        WHERE user_id = %s
                          AND YEAR(expense_date) = %s
                    """, (user_id, year))

                else:

                    cursor.execute("""
                        SELECT COALESCE(SUM(amount), 0) AS spent
                        FROM expenses
                        WHERE user_id = %s
                          AND category = %s
                          AND YEAR(expense_date) = %s
                    """, (user_id, category, year))

            # ------------------------------------------------
            # WEEKLY BUDGET
            # ------------------------------------------------
            elif period == "Weekly":

                if category == "Overall":

                    cursor.execute("""
                        SELECT COALESCE(SUM(amount), 0) AS spent
                        FROM expenses
                        WHERE user_id = %s
                          AND YEAR(expense_date) = %s
                          AND MONTH(expense_date) = %s
                          AND WEEK(expense_date, 1) =
                              WEEK(
                                  STR_TO_DATE(
                                      CONCAT(%s, '-01'),
                                      '%%Y-%%m-%%d'
                                  ),
                                  1
                              )
                    """, (user_id, year, month, f"{year}-{month:02d}"))

                else:

                    cursor.execute("""
                        SELECT COALESCE(SUM(amount), 0) AS spent
                        FROM expenses
                        WHERE user_id = %s
                          AND category = %s
                          AND YEAR(expense_date) = %s
                          AND MONTH(expense_date) = %s
                          AND WEEK(expense_date, 1) =
                              WEEK(
                                  STR_TO_DATE(
                                      CONCAT(%s, '-01'),
                                      '%%Y-%%m-%%d'
                                  ),
                                  1
                              )
                    """, (
                        user_id,
                        category,
                        year,
                        month,
                        f"{year}-{month:02d}"
                    ))

            else:
                cursor.execute(
                    "SELECT 0 AS spent"
                )

            spent_result = cursor.fetchone()

            budget["spent"] = float(spent_result["spent"] or 0)
            budget["amount"] = float(budget["amount"] or 0)

            # Convert dates to strings for JSON
            if budget["budget_month"]:
                budget["budget_month"] = str(budget["budget_month"])

            if budget["created_at"]:
                budget["created_at"] = str(budget["created_at"])

        cursor.close()
        conn.close()

        return jsonify(budgets), 200

    except Exception as e:

        print("Budget GET error:", e)

        return jsonify({
            "message": "Failed to load budgets",
            "error": str(e)
        }), 500


# ============================================================
# CREATE BUDGET
# ============================================================

@app.route("/api/budgets", methods=["POST"])
@login_required
def create_budget():

    user_id = session["user_id"]

    data = request.get_json(silent=True) or {}

    category = data.get("category")
    amount = data.get("amount")
    period = data.get("period")
    budget_month = data.get("budget_month")

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if not category:
        return jsonify({
            "message": "Budget category is required"
        }), 400

    if amount is None:
        return jsonify({
            "message": "Budget amount is required"
        }), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({
            "message": "Budget amount must be a valid number"
        }), 400

    if amount <= 0:
        return jsonify({
            "message": "Budget amount must be greater than 0"
        }), 400

    allowed_categories = {
        "Overall",
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Entertainment",
        "Health",
        "Education",
        "Travel",
        "Rent",
        "Other"
    }

    if category not in allowed_categories:
        return jsonify({
            "message": "Invalid budget category"
        }), 400

    allowed_periods = {
        "Monthly",
        "Weekly",
        "Yearly"
    }

    if period not in allowed_periods:
        return jsonify({
            "message": "Invalid budget period"
        }), 400

    if not budget_month:
        return jsonify({
            "message": "Budget month is required"
        }), 400

    # HTML gives us YYYY-MM.
    # MySQL DATE needs YYYY-MM-01.
    if len(budget_month) == 7:
        budget_month = budget_month + "-01"

    # --------------------------------------------------------
    # Save budget
    # --------------------------------------------------------

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO budgets
                (
                    user_id,
                    category,
                    amount,
                    period,
                    budget_month
                )
            VALUES
                (%s, %s, %s, %s, %s)
        """, (
            user_id,
            category,
            amount,
            period,
            budget_month
        ))

        conn.commit()

        budget_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Budget created successfully.",
            "id": budget_id
        }), 201

    except Exception as e:

        print("Budget POST error:", e)

        return jsonify({
            "message": "Failed to create budget",
            "error": str(e)
        }), 500


# ============================================================
# DELETE BUDGET
# ============================================================

@app.route("/api/budgets/<int:budget_id>", methods=["DELETE"])
@login_required
def delete_budget(budget_id):

    user_id = session["user_id"]

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM budgets
            WHERE id = %s
              AND user_id = %s
        """, (
            budget_id,
            user_id
        ))

        conn.commit()

        if cursor.rowcount == 0:

            cursor.close()
            conn.close()

            return jsonify({
                "message": "Budget not found"
            }), 404

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Budget deleted successfully."
        }), 200

    except Exception as e:

        print("Budget DELETE error:", e)

        return jsonify({
            "message": "Failed to delete budget",
            "error": str(e)
        }), 500


@app.route("/api/budgets/<int:budget_id>", methods=["PUT"])
def update_budget(budget_id):

    if "user_id" not in session:
        return jsonify({"success": False, "message": "You must be logged in to update a budget"}), 401

    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}

    category = data.get("category")
    amount = data.get("amount")
    period = data.get("period") or "Monthly"
    budget_month = data.get("budget_month")

    if not category or amount is None or not period or not budget_month:
        return jsonify({"success": False, "message": "Category, amount, period and budget month are required"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Amount must be a number"}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than zero"}), 400

    if len(str(budget_month)) == 7:
        budget_month = str(budget_month) + "-01"

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE budgets
            SET category = %s, amount = %s, period = %s, budget_month = %s
            WHERE id = %s AND user_id = %s
            """,
            (category, amount, period, budget_month, budget_id, user_id)
        )
        connection.commit()

        cursor.execute("SELECT id FROM budgets WHERE id = %s AND user_id = %s", (budget_id, user_id))
        exists = cursor.fetchone() is not None

        if not exists:
            return jsonify({"success": False, "message": "Budget entry not found"}), 404

        return jsonify({"success": True, "message": "Budget updated successfully"}), 200

    except Exception as e:
        if connection:
            connection.rollback()
        print("Budget PUT error:", e)
        return jsonify({"success": False, "message": "Failed to update budget", "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route("/reports")
@login_required
def reports_page():
    return render_template("reports.html")


@app.route("/api/reports", methods=["GET"])
@login_required
def get_reports():

    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, source, amount, category, income_date
        FROM income
        WHERE user_id = %s
        ORDER BY income_date DESC
    """, (user_id,))

    income = cursor.fetchall()

    cursor.execute("""
        SELECT id, description, amount, category, expense_date
        FROM expenses
        WHERE user_id = %s
        ORDER BY expense_date DESC
    """, (user_id,))

    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    for item in income:
        item["amount"] = float(item["amount"])
        item["income_date"] = str(item["income_date"])

    for item in expenses:
        item["amount"] = float(item["amount"])
        item["expense_date"] = str(item["expense_date"])

    return jsonify({
        "income": income,
        "expenses": expenses
    })

# =========================
# GOALS PAGE
# =========================

@app.route("/goals")
@login_required
def goals_page():
    return render_template("goals.html")


# GET ALL GOALS
@app.route("/api/goals", methods=["GET"])
@login_required
def get_goals():

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            name,
            target_amount,
            saved_amount,
            deadline,
            category,
            icon,
            notes,
            created_at
        FROM goals
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    goals = cursor.fetchall()

    cursor.close()
    conn.close()

    for goal in goals:
        goal["target_amount"] = float(goal["target_amount"])
        goal["saved_amount"] = float(goal["saved_amount"])

        if goal["deadline"]:
            goal["deadline"] = str(goal["deadline"])

        if goal["created_at"]:
            goal["created_at"] = str(goal["created_at"])

    return jsonify({
        "goals": goals
    })


# CREATE GOAL
@app.route("/api/goals", methods=["POST"])
@login_required
def create_goal():

    user_id = session["user_id"]
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data received"
        }), 400

    name = str(data.get("name", "")).strip()
    target_amount = data.get("target_amount", 0)
    saved_amount = data.get("saved_amount", 0)
    deadline = data.get("deadline") or None
    category = data.get("category", "Savings")
    icon = data.get("icon", "🎯")
    notes = data.get("notes", "").strip()

    # Validation
    if not name:
        return jsonify({
            "message": "Goal name is required"
        }), 400

    try:
        target_amount = float(target_amount)
        saved_amount = float(saved_amount)
    except (TypeError, ValueError):
        return jsonify({
            "message": "Invalid amount"
        }), 400

    if target_amount <= 0:
        return jsonify({
            "message": "Target amount must be greater than 0"
        }), 400

    if saved_amount < 0:
        return jsonify({
            "message": "Saved amount cannot be negative"
        }), 400

    if saved_amount > target_amount:
        return jsonify({
            "message": "Saved amount cannot exceed target amount"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO goals
        (
            user_id,
            name,
            target_amount,
            saved_amount,
            deadline,
            category,
            icon,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        name,
        target_amount,
        saved_amount,
        deadline,
        category,
        icon,
        notes
    ))

    conn.commit()

    goal_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Goal created successfully",
        "id": goal_id
    }), 201


# UPDATE GOAL / ADD SAVINGS
@app.route("/api/goals/<int:goal_id>", methods=["PUT"])
@login_required
def update_goal(goal_id):

    user_id = session["user_id"]
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data received"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check that goal belongs to logged-in user
    cursor.execute("""
        SELECT *
        FROM goals
        WHERE id = %s AND user_id = %s
    """, (goal_id, user_id))

    goal = cursor.fetchone()

    if not goal:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Goal not found"
        }), 404

    # Current values
    name = data.get("name", goal["name"])
    target_amount = data.get(
        "target_amount",
        goal["target_amount"]
    )
    saved_amount = data.get(
        "saved_amount",
        goal["saved_amount"]
    )
    deadline = data.get(
        "deadline",
        goal["deadline"]
    )
    category = data.get(
        "category",
        goal["category"]
    )
    icon = data.get(
        "icon",
        goal["icon"]
    )
    notes = data.get(
        "notes",
        goal["notes"]
    )

    try:
        target_amount = float(target_amount)
        saved_amount = float(saved_amount)
    except (TypeError, ValueError):
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Invalid amount"
        }), 400

    if target_amount <= 0:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Target amount must be greater than 0"
        }), 400

    if saved_amount < 0:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Saved amount cannot be negative"
        }), 400

    if saved_amount > target_amount:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Saved amount cannot exceed target amount"
        }), 400

    cursor.execute("""
        UPDATE goals
        SET
            name = %s,
            target_amount = %s,
            saved_amount = %s,
            deadline = %s,
            category = %s,
            icon = %s,
            notes = %s
        WHERE id = %s AND user_id = %s
    """, (
        name,
        target_amount,
        saved_amount,
        deadline,
        category,
        icon,
        notes,
        goal_id,
        user_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Goal updated successfully"
    })


# DELETE GOAL
@app.route("/api/goals/<int:goal_id>", methods=["DELETE"])
@login_required
def delete_goal(goal_id):

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM goals
        WHERE id = %s AND user_id = %s
    """, (goal_id, user_id))

    conn.commit()

    deleted = cursor.rowcount

    cursor.close()
    conn.close()

    if deleted == 0:
        return jsonify({
            "message": "Goal not found"
        }), 404

    return jsonify({
        "message": "Goal deleted successfully"
    })

# ============================================================
# SETTINGS PAGE
# ============================================================

@app.route("/settings")
@login_required
def settings_page():
    return render_template("settings.html")


# ============================================================
# GET SETTINGS
# ============================================================

@app.route("/api/settings", methods=["GET"])
@login_required
def get_settings():

    user_id = session["user_id"]

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get user profile
        cursor.execute("""
            SELECT id, first_name, last_name, email
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()

            session.pop("user_id", None)

            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        # Get preferences
        cursor.execute("""
            SELECT
                currency,
                date_format,
                dark_mode,
                compact_layout,
                show_summary,
                show_goals,
                budget_alerts,
                goal_reminders,
                monthly_summary,
                security_notifications
            FROM user_preferences
            WHERE user_id = %s
        """, (user_id,))

        preferences = cursor.fetchone()

        # Create default preferences if none exist
        if not preferences:

            cursor.execute("""
                INSERT INTO user_preferences
                (user_id)
                VALUES (%s)
            """, (user_id,))

            conn.commit()

            preferences = {
                "currency": "INR",
                "date_format": "DD/MM/YYYY",
                "dark_mode": False,
                "compact_layout": False,
                "show_summary": True,
                "show_goals": True,
                "budget_alerts": True,
                "goal_reminders": True,
                "monthly_summary": True,
                "security_notifications": True
            }

        else:

            # Convert MySQL boolean values to Python bool
            preferences["dark_mode"] = bool(
                preferences["dark_mode"]
            )

            preferences["compact_layout"] = bool(
                preferences["compact_layout"]
            )

            preferences["show_summary"] = bool(
                preferences["show_summary"]
            )

            preferences["show_goals"] = bool(
                preferences["show_goals"]
            )

            preferences["budget_alerts"] = bool(
                preferences["budget_alerts"]
            )

            preferences["goal_reminders"] = bool(
                preferences["goal_reminders"]
            )

            preferences["monthly_summary"] = bool(
                preferences["monthly_summary"]
            )

            preferences["security_notifications"] = bool(
                preferences["security_notifications"]
            )

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "user": user,
            "preferences": preferences
        }), 200

    except Exception as e:

        print("Settings GET error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to load settings",
            "error": str(e)
        }), 500


# ============================================================
# UPDATE PROFILE
# ============================================================

@app.route("/api/settings/profile", methods=["PUT"])
@login_required
def update_profile():

    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}

    first_name = str(
        data.get("first_name", "")
    ).strip()

    last_name = str(
        data.get("last_name", "")
    ).strip()

    email = str(
        data.get("email", "")
    ).strip().lower()

    if not first_name or not last_name or not email:

        return jsonify({
            "success": False,
            "message": "All profile fields are required"
        }), 400

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if another account already uses this email
        cursor.execute("""
            SELECT id
            FROM users
            WHERE email = %s
              AND id != %s
        """, (email, user_id))

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()
            conn.close()

            return jsonify({
                "success": False,
                "message": "Email address is already in use"
            }), 409

        # Update profile
        cursor.execute("""
            UPDATE users
            SET
                first_name = %s,
                last_name = %s,
                email = %s
            WHERE id = %s
        """, (
            first_name,
            last_name,
            email,
            user_id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "user": {
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
        }), 200

    except Exception as e:

        print("Profile update error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to update profile",
            "error": str(e)
        }), 500


# ============================================================
# UPDATE PREFERENCES
# ============================================================

@app.route("/api/settings/preferences", methods=["PUT"])
@login_required
def update_preferences():

    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}

    currency = data.get("currency", "INR")
    date_format = data.get("date_format", "DD/MM/YYYY")

    dark_mode = bool(
        data.get("dark_mode", False)
    )

    compact_layout = bool(
        data.get("compact_layout", False)
    )

    show_summary = bool(
        data.get("show_summary", True)
    )

    show_goals = bool(
        data.get("show_goals", True)
    )

    allowed_currencies = {
        "INR",
        "USD",
        "EUR",
        "GBP"
    }

    if currency not in allowed_currencies:

        return jsonify({
            "success": False,
            "message": "Invalid currency"
        }), 400

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO user_preferences
            (
                user_id,
                currency,
                date_format,
                dark_mode,
                compact_layout,
                show_summary,
                show_goals
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)

            ON DUPLICATE KEY UPDATE
                currency = VALUES(currency),
                date_format = VALUES(date_format),
                dark_mode = VALUES(dark_mode),
                compact_layout = VALUES(compact_layout),
                show_summary = VALUES(show_summary),
                show_goals = VALUES(show_goals)
        """, (
            user_id,
            currency,
            date_format,
            dark_mode,
            compact_layout,
            show_summary,
            show_goals
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Preferences saved successfully"
        }), 200

    except Exception as e:

        print("Preferences update error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to save preferences",
            "error": str(e)
        }), 500


# ============================================================
# UPDATE NOTIFICATIONS
# ============================================================

@app.route("/api/settings/notifications", methods=["PUT"])
@login_required
def update_notifications():

    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}

    budget_alerts = bool(
        data.get("budget_alerts", True)
    )

    goal_reminders = bool(
        data.get("goal_reminders", True)
    )

    monthly_summary = bool(
        data.get("monthly_summary", True)
    )

    security_notifications = bool(
        data.get("security_notifications", True)
    )

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO user_preferences
            (
                user_id,
                budget_alerts,
                goal_reminders,
                monthly_summary,
                security_notifications
            )
            VALUES
            (%s, %s, %s, %s, %s)

            ON DUPLICATE KEY UPDATE
                budget_alerts = VALUES(budget_alerts),
                goal_reminders = VALUES(goal_reminders),
                monthly_summary = VALUES(monthly_summary),
                security_notifications =
                    VALUES(security_notifications)
        """, (
            user_id,
            budget_alerts,
            goal_reminders,
            monthly_summary,
            security_notifications
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Notification settings saved successfully"
        }), 200

    except Exception as e:

        print("Notification update error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to save notification settings",
            "error": str(e)
        }), 500


# ============================================================
# CHANGE PASSWORD
# ============================================================

@app.route("/api/settings/password", methods=["PUT"])
@login_required
def change_password():

    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}

    current_password = data.get(
        "current_password", ""
    )

    new_password = data.get(
        "new_password", ""
    )

    if not current_password or not new_password:

        return jsonify({
            "success": False,
            "message": "All password fields are required"
        }), 400

    if len(new_password) < 8:

        return jsonify({
            "success": False,
            "message": "New password must be at least 8 characters"
        }), 400

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get current password
        cursor.execute("""
            SELECT password
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:

            cursor.close()
            conn.close()

            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        # Check current password
        if not check_password_hash(
            user["password"],
            current_password
        ):

            cursor.close()
            conn.close()

            return jsonify({
                "success": False,
                "message": "Current password is incorrect"
            }), 401

        # Hash new password
        hashed_password = generate_password_hash(
            new_password
        )

        cursor.execute("""
            UPDATE users
            SET password = %s
            WHERE id = %s
        """, (
            hashed_password,
            user_id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Password changed successfully"
        }), 200

    except Exception as e:

        print("Password change error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to change password",
            "error": str(e)
        }), 500


# ============================================================
# DELETE ACCOUNT
# ============================================================

@app.route("/api/account", methods=["DELETE"])
@login_required
def delete_account():

    user_id = session["user_id"]

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        # Because your other tables use:
        # FOREIGN KEY (user_id)
        # REFERENCES users(id)
        # ON DELETE CASCADE
        #
        # deleting the user also deletes:
        # income
        # expenses
        # budgets
        # goals
        # user_preferences

        cursor.execute("""
            DELETE FROM users
            WHERE id = %s
        """, (user_id,))

        conn.commit()

        deleted = cursor.rowcount > 0

        cursor.close()
        conn.close()

        if not deleted:

            session.clear()

            return jsonify({
                "success": False,
                "message": "Account not found"
            }), 404

        # Log user out
        session.clear()

        return jsonify({
            "success": True,
            "message": "Account deleted successfully"
        }), 200

    except Exception as e:

        print("Account deletion error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to delete account",
            "error": str(e)
        }), 500


# ============================================================
# DELETE MY DATA (Retain user account, clear financial data)
# ============================================================

@app.route("/api/account/data", methods=["DELETE"])
@app.route("/api/data", methods=["DELETE"])
@login_required
def delete_user_data():

    user_id = session["user_id"]
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM income WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM expenses WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM budgets WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM goals WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM notifications WHERE user_id = %s", (user_id,))
        cursor.execute("UPDATE users SET data_deleted_at = NOW() WHERE id = %s", (user_id,))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "All your financial data has been deleted."
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()

        print("Data deletion error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to delete financial data",
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ============================================================
# NOTIFICATIONS
# ============================================================

def _budget_spent(cursor, user_id, category, period, year, month):
    """Same spending logic as get_budgets(), so numbers match the Budget page."""
    sql = "SELECT COALESCE(SUM(amount), 0) AS spent FROM expenses WHERE user_id = %s"
    params = [user_id]

    if category != "Overall":
        sql += " AND category = %s"
        params.append(category)

    if period == "Yearly":
        sql += " AND YEAR(expense_date) = %s"
        params.append(year)
    elif period == "Weekly":
        sql += (
            " AND YEAR(expense_date) = %s AND MONTH(expense_date) = %s"
            " AND WEEK(expense_date, 1) = WEEK(STR_TO_DATE(CONCAT(%s, '-01'), '%%Y-%%m-%%d'), 1)"
        )
        params.extend([year, month, f"{year}-{month:02d}"])
    else:  # Monthly
        sql += " AND YEAR(expense_date) = %s AND MONTH(expense_date) = %s"
        params.extend([year, month])

    cursor.execute(sql, tuple(params))
    return float(cursor.fetchone()["spent"] or 0)


def create_notification(cursor, user_id, ntype, title, message,
                        severity="info", reference_id=0, period=""):
    """INSERT IGNORE + UNIQUE KEY means the same alert is created only once
    per (user, type, reference, period)."""
    cursor.execute(
        """
        INSERT IGNORE INTO notifications
        (user_id, type, title, message, severity, reference_id, period)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (user_id, ntype, title, message, severity, reference_id, period)
    )


def generate_budget_notifications(cursor, user_id):
    """Creates 80% (warning) and 100% (danger) alerts for CURRENT-period budgets.
    cursor must be a dictionary cursor."""

    # Respect the Settings > Notifications > Budget alerts toggle
    cursor.execute("SELECT budget_alerts FROM user_preferences WHERE user_id = %s", (user_id,))
    pref = cursor.fetchone()
    if pref is not None and not pref["budget_alerts"]:
        return

    cursor.execute(
        "SELECT id, category, amount, period, budget_month FROM budgets WHERE user_id = %s",
        (user_id,)
    )
    budgets = cursor.fetchall()
    now = datetime.now()

    for b in budgets:
        limit_amt = float(b["amount"] or 0)
        if limit_amt <= 0:
            continue

        bm = b["budget_month"]
        if hasattr(bm, "year"):
            year, month = bm.year, bm.month
        else:
            year, month = int(str(bm)[:4]), int(str(bm)[5:7])

        # Only alert for budgets that apply right now
        if b["period"] == "Yearly":
            if year != now.year:
                continue
            period_key = str(year)
        else:
            if year != now.year or month != now.month:
                continue
            period_key = f"{year}-{month:02d}" + ("-W" if b["period"] == "Weekly" else "")

        spent = _budget_spent(cursor, user_id, b["category"], b["period"], year, month)
        pct = spent / limit_amt * 100
        label = "overall" if b["category"] == "Overall" else b["category"]

        if pct >= 100:
            over = spent - limit_amt
            create_notification(
                cursor, user_id, "budget_100",
                "Budget exceeded",
                f"You have gone over your {label} budget by \u20b9{over:,.0f} (\u20b9{spent:,.0f} of \u20b9{limit_amt:,.0f}).",
                "danger", b["id"], period_key
            )
        elif pct >= 80:
            create_notification(
                cursor, user_id, "budget_80",
                "Budget almost used",
                f"You have used {pct:.0f}% of your {label} budget (\u20b9{spent:,.0f} of \u20b9{limit_amt:,.0f}).",
                "warning", b["id"], period_key
            )


@app.route("/api/notifications", methods=["GET"])
def get_notifications():

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    user_id = session["user_id"]
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create any new alerts first, then return the list
        generate_budget_notifications(cursor, user_id)
        conn.commit()

        cursor.execute(
            """
            SELECT id, type, title, message, severity, is_read, created_at
            FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC, id DESC
            LIMIT 30
            """,
            (user_id,)
        )
        rows = cursor.fetchall()

        cursor.execute(
            "SELECT COUNT(*) AS c FROM notifications WHERE user_id = %s AND is_read = 0",
            (user_id,)
        )
        unread = cursor.fetchone()["c"]

        notifications = [
            {
                "id": r["id"],
                "type": r["type"],
                "title": r["title"],
                "message": r["message"],
                "severity": r["severity"],
                "is_read": bool(r["is_read"]),
                "created_at": r["created_at"].isoformat() if r["created_at"] else None
            }
            for r in rows
        ]

        return jsonify({
            "success": True,
            "unread_count": unread,
            "notifications": notifications
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()
        print("Notifications GET error:", e)
        return jsonify({"success": False, "message": "Failed to load notifications"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/api/notifications/read-all", methods=["POST"])
def read_all_notifications():

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE notifications SET is_read = 1 WHERE user_id = %s AND is_read = 0",
        (session["user_id"],)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"success": True}), 200


@app.route("/api/notifications/<int:notification_id>/read", methods=["POST"])
def read_notification(notification_id):

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE notifications SET is_read = 1 WHERE id = %s AND user_id = %s",
        (notification_id, session["user_id"])
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"success": True}), 200


@app.route("/api/notifications/<int:notification_id>", methods=["DELETE"])
def delete_notification(notification_id):

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM notifications WHERE id = %s AND user_id = %s",
        (notification_id, session["user_id"])
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"success": True}), 200


@app.route("/pricing")
def pricing_page():
    return redirect(url_for("contact_page"))


# ============================================================
# ERROR HANDLING SYSTEM & UTILITY ROUTES
# ============================================================

def render_error(status_code, title, message):
    """Unified error response generator for both JSON APIs and HTML browser views."""
    if wants_json():
        return jsonify({
            "success": False,
            "error": title,
            "message": message,
            "status_code": status_code
        }), status_code

    template_name = "500.html" if status_code >= 500 else "404.html"
    return render_template(
        template_name,
        error_code=status_code,
        error_title=title,
        error_message=message
    ), status_code


@app.route("/logout", methods=["GET", "POST"])
def logout_page_route():
    """Universal logout endpoint handling both GET navigations and POST fetch requests."""
    session.clear()
    if wants_json():
        return jsonify({"success": True, "message": "Logged out successfully"}), 200
    return redirect(url_for("login_page"))


@app.route("/404")
def show_404():
    """Direct route to preview or redirect to the 404 page."""
    return render_error(
        404,
        "Page Not Found",
        "The page you are looking for does not exist, has been moved, or the link you followed is incorrect."
    )


@app.route("/500")
def show_500():
    """Direct route to preview or redirect to the 500 server error page."""
    return render_error(
        500,
        "Internal Server Error",
        "Something unexpected happened on our server while processing your request. Please try reloading or check back in a moment."
    )


@app.errorhandler(400)
def bad_request(e):
    msg = getattr(e, "description", None) or "The request was invalid, malformed, or missing required parameters."
    return render_error(400, "Bad Request", msg)


@app.errorhandler(401)
def unauthorized(e):
    msg = getattr(e, "description", None) or "You must be logged in to view or perform this action."
    return render_error(401, "Unauthorized", msg)


@app.errorhandler(403)
def forbidden(e):
    msg = getattr(e, "description", None) or "You do not have administrative permission to access this resource."
    return render_error(403, "Access Forbidden", msg)


@app.errorhandler(404)
def not_found(e):
    msg = getattr(e, "description", None) or "The page or resource you requested could not be found."
    return render_error(404, "Page Not Found", msg)


@app.errorhandler(405)
def method_not_allowed(e):
    msg = getattr(e, "description", None) or "The requested HTTP method is not allowed for this route."
    return render_error(405, "Method Not Allowed", msg)


@app.errorhandler(408)
def request_timeout(e):
    return render_error(408, "Request Timeout", "The server timed out waiting for the request to complete.")


@app.errorhandler(413)
def payload_too_large(e):
    return render_error(413, "Payload Too Large", "The uploaded request payload exceeds the allowed server limit.")


@app.errorhandler(429)
def too_many_requests(e):
    return render_error(429, "Too Many Requests", "Too many requests. Please slow down and try again shortly.")


@app.errorhandler(500)
def internal_server_error(e):
    msg = getattr(e, "description", None) or "An unexpected server error occurred while processing your request."
    return render_error(500, "Internal Server Error", msg)


@app.errorhandler(502)
def bad_gateway(e):
    return render_error(502, "Bad Gateway", "The server received an invalid response from an upstream server.")


@app.errorhandler(503)
def service_unavailable(e):
    return render_error(503, "Service Unavailable", "The service is temporarily unavailable. Please try again shortly.")


@app.errorhandler(Exception)
def unhandled_exception(e):
    # If it's a known Werkzeug HTTPException, honor its code and message
    if isinstance(e, HTTPException):
        return render_error(e.code, e.name, e.description)

    # Log critical unhandled exceptions for developer debugging
    print("CRITICAL UNHANDLED EXCEPTION:")
    traceback.print_exc()

    return render_error(
        500,
        "Internal Server Error",
        "A critical error occurred while processing your request. Our engineers have been alerted."
    )


if __name__ == "__main__":
    if os.getenv("INIT_DB", "1") == "1":
        try:
            init_db()
        except Exception as exc:
            print("DB init skipped:", exc)
    app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1", port=int(os.getenv("PORT", "5000")))