# dbprocedures

A lightweight Python library that fetches a registered SQL query by name from a MySQL table and returns its result as a **pandas DataFrame**.

---

## Installation

```bash
pip install dbprocedures
```

### For local development
```bash
pip install -e /path/to/dbprocedures/
```

---

## Prerequisites

### 1. Environment Variables

Set the following environment variables before using the library.


| Variable      | Description                        | Example                        |
|---------------|------------------------------------|--------------------------------|
| `DB_HOST`     | MySQL server hostname              | `your-db-host.example.com`     |
| `DB_PORT`     | MySQL server port                  | `3306`                         |
| `DB_NAME`     | Database name                      | `your_database_name`           |
| `DB_USER`     | MySQL username                     | `your_username`                |
| `DB_PASSWORD` | MySQL password                     | `yourpassword`                 |

**Linux / macOS:**
```bash
export DB_HOST=your-db-host.example.com
export DB_PORT=3306
export DB_NAME=your_database_name
export DB_USER=your_username
export DB_PASSWORD=yourpassword
```

**Windows (PowerShell):**
```powershell
$env:DB_HOST = "your-db-host.example.com"
$env:DB_PORT = "3306"
$env:DB_NAME = "your_database_name"
$env:DB_USER = "your_username"
$env:DB_PASSWORD = "yourpassword"
```

### 2. Registry Table

The MySQL database must have a table (default name: `proc_query_registry`) with these columns:

| Column       | Type    | Description                          |
|--------------|---------|--------------------------------------|
| `proc_name`  | VARCHAR | Unique name for the query            |
| `query`      | TEXT    | The SQL query to execute             |

Example:
```sql
CREATE TABLE proc_query_registry (
    proc_name VARCHAR(255) PRIMARY KEY,
    query     TEXT NOT NULL
);
```

> **Important:** All registered queries **must contain a `WHERE` clause**. The library will raise a `ValueError` if a query is registered without one.

---

## Usage

```python
from dbprocedures import call_proc

df = call_proc("my_proc_name")
print(df.head())
```

### Custom registry table name
```python
df = call_proc("my_proc_name", registry_table="my_custom_table")
```

---

## Enabling Debug Logs

The library uses Python's standard `logging` module and produces no output by default. To see connection and query details, enable `DEBUG` logging in your script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from dbprocedures import call_proc

df = call_proc("my_proc_name")
```

---

## How It Works

1. Reads DB credentials from environment variables (and `.env` if present).
2. Connects to MySQL using `pymysql`.
3. Looks up the SQL query in `proc_query_registry` where `proc_name` matches.
4. Validates that the registered query contains a `WHERE` clause.
5. Executes that query on the same DB connection.
6. Returns the result as a `pandas.DataFrame`.
