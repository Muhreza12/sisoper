# db.py — adapter agar project lama tetap jalan (tidak lagi import `config`)
from app_db import (
    connect,
    setup_database,
    user_exists,
    create_user,
    verify_user,
    DATABASE_URL,
)
def get_db_config():
    return ("postgres", {"dsn": DATABASE_URL})
