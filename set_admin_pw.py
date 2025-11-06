
#!/usr/bin/env python3
"""
set_admin_pw.py
Upsert an admin user into the Railway/Postgres database used by your app.
Usage:
    1) Ensure DATABASE_URL environment variable is set (Railway provides it).
    2) Run: python set_admin_pw.py
This will create or update the user with the given username and password.
"""

import os
import hashlib
import psycopg2
from psycopg2 import sql

# === CONFIGURE BELOW ===
USERNAME = "rezaadmin"   # provided by user
NEW_PASSWORD = "reza1212"  # provided by user
ROLE = "admin"
# =======================

def get_dsn():
    dsn = os.getenv("DATABASE_URL") or os.getenv("RAILWAY_DATABASE_URL")
    if not dsn:
        raise SystemExit("ERROR: DATABASE_URL (or RAILWAY_DATABASE_URL) environment variable is not set.")
    return dsn

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def upsert_admin(dsn: str, username: str, password_hash: str, role: str):
    # Connect with sslmode=require to match db.py behaviour on Railway
    conn = psycopg2.connect(dsn, sslmode=os.getenv("PGSSLMODE","require"))
    try:
        cur = conn.cursor()
        # Ensure table exists (same schema as db.py)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(64) NOT NULL,
                role VARCHAR(10) NOT NULL DEFAULT 'user'
            );
        """)
        # Upsert user: update if exists otherwise insert
        cur.execute(sql.SQL("""
            INSERT INTO users (username, password, role) VALUES (%s, %s, %s)
            ON CONFLICT (username) DO UPDATE SET password = EXCLUDED.password, role = EXCLUDED.role;
        """), (username.lower(), password_hash, role))
        conn.commit()
        cur.close()
        print(f"✅ User '{username}' upserted as role='{role}'.")
    finally:
        conn.close()

if __name__ == "__main__":
    dsn = get_dsn()
    h = hash_pw(NEW_PASSWORD)
    upsert_admin(dsn, USERNAME, h, ROLE)
