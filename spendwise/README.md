# SpendWise

Personal finance tracker: income, expenses, budgets, goals, reports, settings.
Flask + MySQL/MariaDB backend, plain HTML/CSS/JS frontend.

## Structure
```
spendwise/
├── app.py              # Flask app: pages + all /api/* routes
├── db.py               # DB connection + init_db() (reads database/schema.sql)
├── database/schema.sql # All tables in one file
├── templates/          # 14 HTML pages (served by Flask)
├── static/css/ui.css   # shared styles, toggles, motion
├── static/js/ui.js     # icon sprite, page transitions, reveal, live toggles
├── requirements.txt
└── .env.example
```

## Run
```
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then set DB_PASSWORD and SECRET_KEY
python app.py               # creates the database + tables automatically
```
Open http://localhost:5000

## Flow
`/` → `/register` → `/login` → `/dashboard` → `/income` `/expenses` `/budget` `/goals` `/reports` `/settings`.
Protected pages redirect to `/login?next=...` and return you there after login.
Unknown URLs show the 404 page.
