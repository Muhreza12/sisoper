# connect_test.py
import os, psycopg2
dsn = os.getenv("DATABASE_URL")
if not dsn:
    raise SystemExit("DATABASE_URL not set")
conn = psycopg2.connect(dsn, sslmode="require")
with conn.cursor() as cur:
    cur.execute("SELECT version();")
    print("✅", cur.fetchone()[0])
conn.close()
