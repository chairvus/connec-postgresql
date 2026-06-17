# Connecting to PostgreSQL via Python

A simple exercise demonstrating how to connect to a PostgreSQL database from Python using **SQLAlchemy** and **psycopg2**, and how to insert data into a table.

## Overview

This project covers:

- Setting up a local PostgreSQL database (via Homebrew)
- Creating a database engine connection using SQLAlchemy
- Creating a table
- Inserting data into the table
- Querying and displaying the inserted data

## Tech Stack

- Python 3.13
- [SQLAlchemy](https://www.sqlalchemy.org/) — SQL toolkit and ORM
- [psycopg2](https://www.psycopg.org/) — PostgreSQL adapter for Python
- PostgreSQL 16

## Prerequisites

- macOS with [Homebrew](https://brew.sh/) installed
- Python 3.13+ and `pip`

## Setup

### 1. Install PostgreSQL

```bash
brew install postgresql@16
```

Since `postgresql@16` is keg-only, add it to your PATH:

```bash
# bash/zsh
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc

# fish
fish_add_path /opt/homebrew/opt/postgresql@16/bin
```

Restart your terminal, then verify:

```bash
psql --version
```

### 2. Start the PostgreSQL service

```bash
brew services start postgresql@16
```

Check that it's running:

```bash
brew services list
```

### 3. Create the database role and database

This project expects a role named `developer` and a database named `companydb`:

```bash
createuser -s developer
createdb -O developer companydb
psql -d companydb -c "ALTER USER developer WITH PASSWORD 'secretpassword';"
```

> Note: by default, Homebrew's PostgreSQL cluster superuser is your macOS username, not `postgres`. The commands above use that default superuser to create the new role.

### 4. Verify the connection manually (optional)

```bash
psql -U developer -d companydb -h localhost -c "\conninfo"
```

You'll be prompted for the password (`secretpassword`).

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/connecting-to-postgre.git
cd connecting-to-postgre
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .env
source .env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Exercise

```bash
python main.py
```

Expected output:

```
Terhubung dengan basis data!
Tabel 'employees' siap digunakan.
Data baru berhasil ditambahkan!

Isi tabel employees:
(1, 'Arth', 'Data Analyst', Decimal('8000000.00'))
```

## How It Works

`main.py` does the following, in order:

1. **Creates an engine** — `create_engine()` builds a connection string pointing to the local PostgreSQL instance using the `psycopg2` driver.
2. **Opens a connection** — using a `with` block ensures the connection is properly closed afterward, even if an error occurs.
3. **Creates a table** (`employees`) if it doesn't already exist, with columns for `id`, `name`, `position`, and `salary`.
4. **Inserts a row** using a parameterized query (`:name`, `:position`, `:salary`) — this is the safe way to insert data and avoids SQL injection.
5. **Commits the transaction** — SQLAlchemy 2.x requires an explicit `commit()` for write operations (`INSERT`, `CREATE TABLE`, etc.) when not using `engine.begin()`.
6. **Queries the table** and prints all rows to confirm the insert worked.

## Troubleshooting

### `role "developer" does not exist`

This means PostgreSQL is reachable, but the `developer` role hasn't been created yet. Run:

```bash
createuser -s developer
psql -d companydb -c "ALTER USER developer WITH PASSWORD 'secretpassword';"
```

### `database "companydb" does not exist`

```bash
createdb -O developer companydb
```

### `psql: command not found`

`postgresql@16` is keg-only and isn't symlinked into your PATH automatically. See [Step 1 in Setup](#1-install-postgresql) above.

### Connection refused on port 5432

Make sure the PostgreSQL service is actually running:

```bash
brew services start postgresql@16
brew services list
```

## License

This project is for educational purposes.
