# Stage 3 Demo Script (Fitness Scheduler)

Use this as a spoken script. Target 6–8 minutes. Sections: intro, live app, SQLi protections, indexes, transactions/isolation, wrap-up.

## 1) Intro (30–45s)
- “This is Fitness Scheduler, a Django app to track workouts.”
- “I’ll show live CRUD + report, then how I protect against SQL injection, what indexes I added and why, and how I use transactions and isolation.”

## 2) Live App Flow (2–3m)
1. List page: “Here are my sessions, ordered by most recent.” (path: `/`)
2. Add session: click Add → submit a realistic entry. Note duration/intensity fields enforce >0 and 1–5.
3. Edit one item briefly.
4. Delete a throwaway item.
5. Report page (`/report`): run with filters (date range + workout type) and point out the summary stats updating (total sessions, avg duration, avg intensity).

## 3) SQL Injection Protection (1–1.5m)
- Show `scheduler/views.py` queries: `WorkoutSession.objects...` only—no raw SQL.
- Say: “Django ORM parameterizes all queries, so user input never hits SQL directly.”
- Show `scheduler/models.py`: validators on `duration_minutes` and `intensity` (Min/Max) so bad inputs are rejected before reaching the DB.
- Show `scheduler/forms.py`: `ModelChoiceField` for workout_type builds the dropdown from the DB, preventing arbitrary IDs.
- Optional line: “If I ever need raw SQL, I’d use `cursor.execute(sql, [params])` with placeholders, but none exist today.”

## 4) Indexes (1–1.5m)
- Open `scheduler/models.py` Meta.indexes:
  - `session_date_idx` on `date`.
  - `session_type_date_idx` on `(workout_type, date)`.
- Explain usage:
  - List view (`views.session_list`): orders by date; the date index helps scanning recent rows.
  - Report (`views.session_report`): filters by `date__gte`, `date__lte`, `workout_type`; the composite index accelerates this filtered set before aggregates (Count/Avg).
- Mention migration: `0002_workoutsession_indexes.py` adds these indexes; applied via `python manage.py migrate`.
- Justify why they matter (say this):
  - “List view is the home page and runs on every visit; ordering by date benefits from the date index to avoid full scans as data grows.”
  - “Report is the critical analysis feature; users almost always filter by workout type and date range, so the `(workout_type, date)` index supports that exact predicate and keeps the aggregate fast.”

## 5) Transactions & Isolation (1–1.5m)
- Show `mysite/settings.py`: `ATOMIC_REQUESTS=True` → every request is wrapped in a transaction automatically.
- Show `scheduler/views.py`: `transaction.atomic()` around create/update/delete to keep each operation all-or-nothing.
- Concurrency note (justify choice):
  - “On SQLite, writes serialize via DB locks, so concurrent writes are inherently serialized.”
  - “If I deploy to Postgres/MySQL, I’d keep `READ COMMITTED` as the default: it prevents dirty reads and is the right balance for this CRUD app. If reports needed a stable snapshot during long reads, I’d bump report endpoints to `REPEATABLE READ` to avoid seeing mid-transaction changes.”
  - “All writes are wrapped in `atomic()`, so partial saves/deletes can’t leak; either the whole request commits or it rolls back.”

## 6) Commands / How to Run (30s)
- “Create venv → install Django 5.2.8 → migrate → runserver”:
  ```
  python -m venv .venv
  .\.venv\Scripts\activate
  pip install "Django==5.2.8"
  python manage.py migrate
  python manage.py runserver
  ```

## 7) URL
- Local dev: `http://127.0.0.1:8000/`
- Cloud URL (if deployed): `https://<your-app-url>` (extra credit not done here).

## 8) Closing (15–30s)
- “We covered CRUD + reporting, SQL injection protections via the ORM and validators, targeted indexes for list/report queries, and transactions with Django’s atomic requests. Happy to answer questions.” 

---

# Extra Credit (quick deploy plan: Render free tier)
- Why Render: free web service + free Postgres + public URL; delete after grading to avoid charges.
- App is ready: env-based settings (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`), WhiteNoise for static files, `requirements.txt`, `Procfile`.
- Steps:
  1) Push code to GitHub.
  2) In Render: create a free Postgres instance; copy its `DATABASE_URL`.
  3) Create a new Web Service from the repo. Set start command: `gunicorn mysite.wsgi`.
  4) Env vars: `SECRET_KEY=<generate>`, `DEBUG=false`, `ALLOWED_HOSTS=your-app.onrender.com`, `DATABASE_URL=<from Render Postgres>`.
  5) Build commands (auto): `pip install -r requirements.txt`; add a deploy hook/command to run `python manage.py migrate` and `python manage.py collectstatic --noinput` (Render has a “postdeploy” command field).
  6) Deploy. Visit the Render URL and verify: create/edit/delete a session and run the report.
- If using another host, follow the same env vars and start command.
