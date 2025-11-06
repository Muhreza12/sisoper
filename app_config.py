# app_db.py — single module: config reader + DB helpers
import os, sys, configparser, hashlib
from typing import Optional
import psycopg2

def _app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def _load_database_url():
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    ini = os.path.join(_app_dir(), "config.ini")
    if os.path.exists(ini):
        cfg = configparser.ConfigParser()
        cfg.read(ini, encoding="utf-8")
        if "server" in cfg and "DATABASE_URL" in cfg["server"]:
            return cfg["server"]["DATABASE_URL"].strip()
    envp = os.path.join(_app_dir(), ".env")
    if os.path.exists(envp):
        with open(envp, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("DATABASE_URL="):
                    return line.split("=",1)[1].strip().strip('"').strip("'")
    return None

DATABASE_URL = _load_database_url()

def connect():
    if not DATABASE_URL:
        print("❌ DATABASE_URL tidak ditemukan (cek config.ini / .env)")
        return None, None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        return conn, "postgres"
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return None, None

def setup_database():
    conn, _ = connect()
    if not conn:
        print("✖ Cannot setup database: Connection failed")
        return
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(256) NOT NULL,
            role VARCHAR(50) DEFAULT 'user'
        );
    """)
    conn.commit()
    conn.close()
    print("✅ Database setup completed (postgres)")

def user_exists(username: str) -> bool:
    conn, _ = connect()
    if not conn: return False
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username=%s", (username,))
    r = cur.fetchone()
    conn.close()
    return bool(r)

def create_user(username: str, password: str, role: str = "user") -> bool:
    conn, _ = connect()
    if not conn: return False
    cur = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (%s,%s,%s) ON CONFLICT (username) DO NOTHING",
        (username, hashed, role),
    )
    conn.commit()
    conn.close()
    return True

def verify_user(username: str, password: str) -> Optional[str]:
    conn, _ = connect()
    if not conn: return None
    cur = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, hashed))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
