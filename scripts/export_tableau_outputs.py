"""
Export Tableau-ready CSV files from DuckDB using the project SQL layer.

Run from the repository root:
    python scripts/export_tableau_outputs.py

Canonical source: data/ecommerce_orders.csv
Outputs: outputs/tableau/*.csv (semicolon-delimited for French Tableau locale)
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb

# Repository root (parent of scripts/)
REPO_ROOT = Path(__file__).resolve().parent.parent

RAW_CSV = REPO_ROOT / "data" / "ecommerce_orders.csv"
DB_PATH = REPO_ROOT / "data" / "profit_leak.duckdb"
TABLEAU_DIR = REPO_ROOT / "outputs" / "tableau"

SQL_SCHEMA = REPO_ROOT / "sql" / "00_schema.sql"
SQL_STAGING = REPO_ROOT / "sql" / "02_staging_profit_view.sql"

# Analysis queries → Tableau export files
EXPORT_QUERIES: list[tuple[str, str]] = [
    ("sql/03_kpi_overview.sql", "outputs/tableau/kpi_overview.csv"),
    ("sql/04_profit_by_category.sql", "outputs/tableau/profit_by_category.csv"),
    ("sql/05_profit_by_region.sql", "outputs/tableau/profit_by_region.csv"),
    ("sql/06_category_region_segments.sql", "outputs/tableau/category_region_segments.csv"),
    ("sql/07_discount_impact.sql", "outputs/tableau/discount_impact.csv"),
    ("sql/08_top_customers.sql", "outputs/tableau/top_customers.csv"),
    ("sql/09_loss_making_orders.sql", "outputs/tableau/loss_making_orders.csv"),
    ("sql/10_monthly_trend.sql", "outputs/tableau/monthly_trend.csv"),
    ("sql/11_high_discount_impact.sql", "outputs/tableau/high_discount_impact.csv"),
]


def log(message: str) -> None:
    print(message, flush=True)


def read_sql(path: Path) -> str:
    """Read a SQL file and remove trailing semicolons for safe wrapping."""
    sql = path.read_text(encoding="utf-8").strip()
    while sql.endswith(";"):
        sql = sql[:-1].strip()
    return sql


def execute_sql_file(conn: duckdb.DuckDBPyConnection, path: Path) -> None:
    conn.execute(read_sql(path))


def load_ecommerce_orders(conn: duckdb.DuckDBPyConnection, csv_path: Path) -> int:
    """Load canonical CSV into ecommerce_orders (preserves region code NA)."""
    csv_posix = csv_path.as_posix()

    conn.execute("DELETE FROM ecommerce_orders")

    conn.execute(
        f"""
        INSERT INTO ecommerce_orders (
            order_id,
            customer_id,
            product_category,
            region,
            order_date,
            revenue,
            cost,
            discount
        )
        SELECT
            order_id,
            customer_id,
            product_category,
            region,
            CAST(order_date AS DATE)  AS order_date,
            CAST(revenue AS DOUBLE)   AS revenue,
            CAST(cost AS DOUBLE)      AS cost,
            CAST(discount AS DOUBLE)  AS discount
        FROM read_csv(
            '{csv_posix}',
            header  = true,
            delim   = ',',
            columns = {{
                order_id:         'VARCHAR',
                customer_id:      'VARCHAR',
                product_category: 'VARCHAR',
                region:           'VARCHAR',
                order_date:       'VARCHAR',
                revenue:          'DOUBLE',
                cost:             'DOUBLE',
                discount:         'DOUBLE'
            }}
        )
        """
    )

    row_count = conn.execute("SELECT COUNT(*) FROM ecommerce_orders").fetchone()[0]
    na_count = conn.execute(
        "SELECT COUNT(*) FROM ecommerce_orders WHERE region = 'NA'"
    ).fetchone()[0]
    log(f"  -> {row_count:,} orders loaded ({na_count:,} North America / NA region)")
    return row_count


def export_query_to_csv(
    conn: duckdb.DuckDBPyConnection,
    sql_path: Path,
    output_path: Path,
) -> None:
    """Export query results to a semicolon-delimited CSV for Tableau."""
    query = read_sql(sql_path)
    out_posix = output_path.as_posix()

    conn.execute(
        f"""
        COPY ({query})
        TO '{out_posix}'
        (HEADER, DELIMITER ';')
        """
    )


def main() -> int:
    log("Starting Tableau export (DuckDB SQL layer)...")

    if not RAW_CSV.is_file():
        log(f"ERROR: Canonical CSV not found: {RAW_CSV}")
        log("       Generate it with: python scripts/generate_dataset.py")
        return 1

    log(f"Raw CSV found: {RAW_CSV}")

    TABLEAU_DIR.mkdir(parents=True, exist_ok=True)

    # Recreate local database
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = duckdb.connect(str(DB_PATH))
    try:
        log(f"DuckDB database created: {DB_PATH}")

        log("Creating raw table (sql/00_schema.sql)...")
        execute_sql_file(conn, SQL_SCHEMA)

        log("Loading raw data from data/ecommerce_orders.csv...")
        load_ecommerce_orders(conn, RAW_CSV)
        log("Raw data loaded.")

        log("Creating staging view (sql/02_staging_profit_view.sql)...")
        execute_sql_file(conn, SQL_STAGING)
        log("Staging view created: stg_orders_profit")

        log("Exporting Tableau CSV files (semicolon delimiter)...")
        for sql_rel, out_rel in EXPORT_QUERIES:
            sql_path = REPO_ROOT / sql_rel
            out_path = REPO_ROOT / out_rel
            out_path.parent.mkdir(parents=True, exist_ok=True)

            export_query_to_csv(conn, sql_path, out_path)
            log(f"  Exported: {out_rel}")

        log("")
        log("SUCCESS: All Tableau exports written to outputs/tableau/")
        log("         Connect Tableau to these CSVs or to data/profit_leak.duckdb.")
        return 0

    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
