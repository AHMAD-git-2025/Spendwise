# SpendWise — Personal Budget & Expense Manager

Personal finance tracker: income, expenses, budgets, goals, reports, settings, and administration.
Flask + MySQL/MariaDB backend, vanilla HTML/CSS/JS frontend with modern glassmorphism design.

## Structure
```
spendwise/
├── app.py              # Flask app: web routes + /api/* endpoints
├── admin.py            # Admin console routes & table management
├── db.py               # DB connection layer (supports local & cloud/Aiven MySQL)
├── init_db.py          # Cloud & local database initializer
├── database/schema.sql # Complete database tables schema
├── render.yaml         # Render deployment blueprint specification
├── Procfile            # Gunicorn process definition for cloud hosting
├── templates/          # HTML templates (Dashboard, Expenses, Income, Admin, etc.)
├── static/css/ui.css   # Modern design tokens, glassmorphism, animations
├── static/js/ui.js     # Unified UI engine, 60-day policy calendar enforcement
├── requirements.txt
└── .env
```

---

## Local Development

```bash
cd spendwise
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open **http://localhost:5000** in your browser.

---

## Cloud Deployment (Render + Aiven MySQL)

### 1. Set Up Aiven MySQL
1. Create a MySQL database service on [Aiven.io](https://aiven.io).
2. Copy your **Service URI** (or the individual Host, Port, User, Password, and Database `defaultdb`).

### 2. Push Code to GitHub
```bash
git init
git add .
git commit -m "Deploy SpendWise"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 3. Deploy to Render
1. Go to [Render Dashboard](https://dashboard.render.com) and click **New +** → **Web Service**.
2. Connect your GitHub repository.
3. Configure settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python init_db.py`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`
4. Under **Environment Variables**, add:
   - `DATABASE_URL`: Your Aiven Service URI (e.g. `mysql://avnadmin:password@host:port/defaultdb?ssl-mode=REQUIRED`)
     *(or set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME=defaultdb`, `DB_SSL=true`)*
   - `SECRET_KEY`: A secure random secret string
   - `ADMIN_PASSWORD`: Your password for the `/admin` portal
   - `PYTHON_VERSION`: `3.11.8`
5. Click **Create Web Service**. Tables will be initialized automatically in Aiven MySQL upon deployment.
