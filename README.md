# Crypto Insight (PyQt5) — Login Minimal

Aplikasi desktop Python (PyQt5) dengan login dan role **admin** / **user**. Database SQLite otomatis dibuat saat pertama kali dijalankan.

## Akun Bawaan
- **Admin**: `admin` / `admin123`
- **User**: `reza` / `12345`

## Cara Jalankan (PowerShell / CMD / VS Code Terminal)
```bash
cd crypto_insight_pyqt
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

> Jika belum install Python, unduh dari python.org dan pastikan dicentang "Add to PATH".

## Struktur
```
crypto_insight_pyqt/
├─ main.py
├─ db.py
├─ admin_dashboard.py
├─ user_dashboard.py
├─ requirements.txt
└─ database.db  (terbentuk otomatis setelah pertama run)
```

## Catatan
- Password masih **plain text** agar mudah diuji. Untuk produksi, gunakan hashing (bcrypt/argon2).
- Jika layar tidak muncul: cek apakah **PyQt5** sudah terpasang dan jalankan `python main.py` dari folder project.
- Ganti/ tambah user:
  ```sql
  -- buka DB pakai DB Browser for SQLite
  INSERT INTO users (username, password, role) VALUES ('nama', 'pass', 'user');
  ```
