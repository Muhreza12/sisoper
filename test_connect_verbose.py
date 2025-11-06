from app_db import DATABASE_URL
import psycopg2, traceback
print("Using:", DATABASE_URL)
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require", connect_timeout=10)
    print("✅ Connected OK")
    conn.close()
except Exception:
    traceback.print_exc()
