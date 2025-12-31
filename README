# Zoo Project API

FastAPI backend for zoo management with PostgreSQL, SQLAlchemy, and Alembic.

## Structure
```text
.
├── src/               # Application Source
│   ├── main.py        # Entry point (FastAPI app)
│   ├── models.py      # SQLAlchemy Tables
│   └── database.py    # DB Connection & Session
├── scripts/           # Utilities
│   ├── init_db.sql    # Raw SQL for DB creation
│   └── populate_data.py # Seeder script
├── alembic/           # Migrations versions & env
└── alembic.ini        # Migration config
```


## Setup & Run

### 1. Environment

```Bash
# Create & Activate Virtual Env
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 2. Configuration

Open alembic.ini and update the sqlalchemy.url line to match your database credentials:

```ini
sqlalchemy.url = postgresql://user:pass@localhost/dbname
```

### 3. Database Initialization

Ensure PostgreSQL is running.

```Bash
# Create Database (if not exists)
psql -U postgres -f scripts/init_db.sql

# Run Migrations
alembic upgrade head

# (Optional) Seed Data
python scripts/populate_data.py
```

### 4. Run Server

**Note**: Run from the root directory.

```Bash
uvicorn src.main:app --reload
```

Docs: http://127.0.0.1:8000/docs


## Command Cheatsheet

| Action | Command |
| :--- | :--- |
| **New Migration** | `alembic revision --autogenerate -m "message"` |
| **Apply Migration** | `alembic upgrade head` |
| **Undo Migration** | `alembic downgrade -1` |
| **Run Linter** | `flake8 src` |


