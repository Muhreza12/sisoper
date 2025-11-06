Crypto Insight (PyQt) — Paket Distribusi
========================================

Cara menjalankan:
1) Ekstrak file ZIP ini ke folder mana saja (mis. Desktop).
2) Pastikan file `config.ini` ADA di folder yang sama dengan `main.exe`.
3) Klik dua kali `main.exe` untuk menjalankan aplikasi.

Jika koneksi database gagal:
- Buka `config.ini` dan pastikan URL benar dan mengandung `?sslmode=require`.
- Jika kamu pernah mengatur environment variable bernama DATABASE_URL ke localhost,
  hapus dulu env tersebut atau jalankan lewat launcher `run.cmd`.

Struktur folder setelah ekstrak:
- main.exe
- config.ini
- run.cmd  (opsional launcher yang menyetel DATABASE_URL untuk sesi ini)
- README.txt
