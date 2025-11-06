# app_db.py — Railway PostgreSQL helpers + presence + news (penerbit)
import os, sys, configparser, hashlib
from typing import Optional, Tuple, List
import psycopg2

# ---------- Config ----------
def _app_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)  # saat sudah jadi EXE
    return os.path.dirname(os.path.abspath(__file__))

def _load_database_url() -> Optional[str]:
    # 1) config.ini (tahan BOM)
    ini = os.path.join(_app_dir(), "config.ini")
    if os.path.exists(ini):
        cfg = configparser.ConfigParser()
        cfg.read(ini, encoding="utf-8-sig")
        if "server" in cfg and "DATABASE_URL" in cfg["server"]:
            return cfg["server"]["DATABASE_URL"].strip()

    # 2) ENV
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    # 3) .env (opsional)
    envp = os.path.join(_app_dir(), ".env")
    if os.path.exists(envp):
        with open(envp, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("DATABASE_URL="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

DATABASE_URL: Optional[str] = _load_database_url()

# ---------- Core DB ----------
def connect() -> Tuple[Optional[psycopg2.extensions.connection], Optional[str]]:
    if not DATABASE_URL:
        print("❌ DATABASE_URL tidak ditemukan (cek config.ini / .env)")
        return None, None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        return conn, "postgres"
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return None, None

def setup_database() -> None:
    conn, _ = connect()
    if not conn:
        print("✖ Cannot setup database: Connection failed")
        return
    cur = conn.cursor()

    # Tabel users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(256) NOT NULL,
            role VARCHAR(50) DEFAULT 'user'
        );
    """)

    # Tabel presence
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
          id SERIAL PRIMARY KEY,
          username VARCHAR(100) NOT NULL,
          started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
          last_seen  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
          status     VARCHAR(16) NOT NULL DEFAULT 'online'
        );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_username ON user_sessions(username);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_last_seen ON user_sessions(last_seen);")

    # Tabel berita (khusus role 'penerbit')
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
          id SERIAL PRIMARY KEY,
          title VARCHAR(200) NOT NULL,
          content TEXT NOT NULL,
          author VARCHAR(100) NOT NULL,                -- username penerbit
          status VARCHAR(20) NOT NULL DEFAULT 'draft', -- 'draft' / 'published'
          created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_news_created_at ON news(created_at DESC);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_news_author ON news(author);")

    conn.commit()
    conn.close()
    print("✅ Database setup completed (postgres)")

# ---------- Users ----------
def user_exists(username: str) -> bool:
    conn, _ = connect()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username=%s", (username,))
    r = cur.fetchone()
    conn.close()
    return bool(r)

def create_user(username: str, password: str, role: str = "user") -> bool:
    conn, _ = connect()
    if not conn:
        return False
    cur = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (%s,%s,%s) "
        "ON CONFLICT (username) DO NOTHING",
        (username, hashed, role),
    )
    conn.commit()
    conn.close()
    return True

def verify_user(username: str, password: str) -> Optional[str]:
    conn, _ = connect()
    if not conn:
        return None
    cur = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, hashed))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# ---------- Presence (online tracking) ----------
ONLINE_WINDOW_SECONDS = 45  # dianggap online jika heartbeat < 45 detik

def start_session(username: str) -> Optional[int]:
    conn, _ = connect()
    if not conn:
        return None
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO user_sessions (username, status) VALUES (%s, 'online') RETURNING id;",
        (username,)
    )
    sid = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return sid

def heartbeat(session_id: int) -> bool:
    conn, _ = connect()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute("UPDATE user_sessions SET last_seen = NOW() WHERE id = %s;", (session_id,))
    conn.commit()
    conn.close()
    return True

def end_session(session_id: int) -> None:
    conn, _ = connect()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("UPDATE user_sessions SET status='offline', last_seen=NOW() WHERE id=%s;", (session_id,))
    conn.commit()
    conn.close()

def latest_presence_per_user() -> List[tuple]:
    """
    Kembalikan [(username, role, is_online, last_seen_utc), ...]
    """
    conn, _ = connect()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute(f"""
        WITH latest AS (
            SELECT username, MAX(last_seen) AS ls
            FROM user_sessions
            GROUP BY username
        )
        SELECT l.username,
               COALESCE(u.role, 'user') AS role,
               EXISTS(
                 SELECT 1 FROM user_sessions s
                 WHERE s.username = l.username
                   AND s.last_seen = l.ls
                   AND s.status = 'online'
                   AND s.last_seen > NOW() - INTERVAL '{ONLINE_WINDOW_SECONDS} seconds'
               ) AS is_online,
               to_char(l.ls AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI:SS UTC') AS last_seen_utc
        FROM latest l
        LEFT JOIN users u ON u.username = l.username
        ORDER BY l.username;
    """)
    rows = cur.fetchall()
    conn.close()
    return [(r[0], r[1], bool(r[2]), r[3]) for r in rows]

# ---------- NEWS (untuk role 'penerbit') ----------
def create_news(author: str, title: str, content: str, publish: bool = True) -> bool:
    """Simpan berita baru. Jika publish=True -> status='published'."""
    conn, _ = connect()
    if not conn:
        return False
    cur = conn.cursor()
    status = 'published' if publish else 'draft'
    cur.execute(
        "INSERT INTO news (title, content, author, status) VALUES (%s, %s, %s, %s);",
        (title, content, author, status)
    )
    conn.commit(); conn.close()
    return True

def list_my_news(author: str, limit: int = 50) -> List[tuple]:
    """Ambil daftar berita milik author (terbaru dulu)."""
    conn, _ = connect()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, status, to_char(created_at AT TIME ZONE 'UTC','YYYY-MM-DD HH24:MI UTC')
        FROM news
        WHERE author=%s
        ORDER BY created_at DESC
        LIMIT %s;
    """, (author, limit))
    rows = cur.fetchall()
    conn.close()
    return rows  # [(id, title, status, created_at), ...]

def list_published_news(limit: int = 50) -> List[tuple]:
    """(opsional) Ambil feed publik."""
    conn, _ = connect()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, author, to_char(created_at AT TIME ZONE 'UTC','YYYY-MM-DD HH24:MI UTC')
        FROM news
        WHERE status='published'
        ORDER BY created_at DESC
        LIMIT %s;
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
