# db-query-lib

A lightweight Python library that fetches a registered SQL query by name from a MySQL table and returns its result as a **pandas DataFrame**.

---

## Installation

### From a local folder
```bash
pip install /path/to/db_query_lib/
```

### From a Git repository (internal)
```bash
pip install git+https://your-internal-git-repo/db_query_lib.git
```

---

## Prerequisites

### 1. Environment Variables

Set the following environment variables before using the library:

| Variable      | Description                        | Example                                      |
|---------------|------------------------------------|----------------------------------------------|
| `DB_HOST`     | MySQL server hostname              | `your-db-host.example.com`                   |
| `DB_PORT`     | MySQL server port                  | `3306`                                       |
| `DB_NAME`     | Database name                      | `your_database_name`                         |
| `DB_USER`     | MySQL username                     | `your_username`                                  |
| `DB_PASSWORD` | MySQL password                     | `yourpassword`                               |

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

---

## Usage

```python
from db_query_lib import run_proc

df = run_proc("my_proc_name")
print(df.head())
```

### Custom registry table name
```python
df = run_proc("my_proc_name", registry_table="my_custom_table")
```

---

## How It Works

1. Reads DB credentials from environment variables.
2. Connects to MySQL using `pymysql`.
3. Looks up the SQL query in `proc_query_registry` where `proc_name` matches.
4. Executes that query on the same DB connection.
5. Returns the result as a `pandas.DataFrame`.
