# 🔍 TESTING & BUG REPORT - Crypto Insight
**Generated:** 2025-10-31  
**Project Status:** 30% Complete

---

## ✅ TESTING CHECKLIST

### 1. Database Connection
- [ ] Test koneksi ke Railway PostgreSQL
- [ ] Verify config.ini terbaca dengan benar
- [ ] Test table creation (users, user_sessions, news)
- [ ] Test SSL connection requirement

### 2. Authentication System
- [ ] Login dengan user valid
- [ ] Login dengan password salah
- [ ] Login dengan user tidak ada
- [ ] Register user baru (role: user)
- [ ] Register user baru (role: penerbit)
- [ ] Register dengan username duplikat
- [ ] Register dengan password < 4 karakter
- [ ] Toggle show/hide password

### 3. Role-Based Dashboard
- [ ] Admin dashboard - monitoring features
- [ ] User dashboard - basic features
- [ ] Penerbit dashboard - news posting
- [ ] Logout dari setiap dashboard
- [ ] Session tracking (heartbeat)

### 4. Admin Features
- [ ] View user list
- [ ] Auto-refresh user detection
- [ ] Activity monitoring
- [ ] Statistics display
- [ ] Export reports

### 5. Penerbit Features
- [ ] Create news (draft)
- [ ] Create news (published)
- [ ] View own news list
- [ ] News feed display

---

## 🐛 BUGS FOUND

### 🔴 CRITICAL

#### Bug #1: Inkonsistensi Import PyQt
**File:** Hampir semua file
**Issue:** Mixed usage PyQt5/PyQt6
```python
# Di auth_ui.py ada:
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    is_qt6 = False
except Exception:
    from PyQt6 import QtCore, QtGui, QtWidgets
    is_qt6 = True
```
**Problem:** Beberapa file tidak punya fallback ini
**Fix Needed:** Standardisasi ke PyQt5 saja (sesuai requirements.txt)

#### Bug #2: Password Hashing Tidak Konsisten
**File:** `app_db.py` vs old files
**Issue:** 
- `app_db.py` → uses SHA256 hashing ✅
- Password storage: hashed ✅
- Tapi di README.md bilang "plain text" ❌

**Recommendation:** Dokumentasi perlu diupdate

#### Bug #3: Database URL Exposure
**File:** `config.ini`
**Issue:** Credential hardcoded dan ter-push ke code
```ini
DATABASE_URL=postgresql://postgres:WuZnoaOPPcCPpsPQcpJZdiswoenTjoXE@...
```
**SECURITY RISK:** 🚨 Credential terbuka di repository
**Fix Needed:** 
- Add `config.ini` to `.gitignore`
- Use `config.ini.example` template
- Rotate database password

---

### 🟡 MEDIUM PRIORITY

#### Bug #4: User Dashboard Kosong
**File:** `user_dashboard.py`
**Issue:** Hanya placeholder text, tidak ada fitur crypto
```python
info = QtWidgets.QLabel("Ini adalah halaman User Dashboard.\n
    Contoh fitur: lihat harga crypto, berita terbaru, dan portofolio.")
```
**Status:** Expected (30% progress)

#### Bug #5: Multiple Main Files
**Files:** `main.py`, `integrated_main.py`, `integrated_main_with_monitoring.py`
**Issue:** Ada 3 main file berbeda, membingungkan
**Which to use?** `main.py` tampaknya yang official (terhubung ke `auth_ui.py`)

#### Bug #6: Unused/Redundant Files
**Files:**
- `db.py` - wrapper ke `app_db.py`
- `app_config.py` - mirip `app_db.py` tapi tidak lengkap
- Multiple admin dashboard versions

**Recommendation:** Cleanup & consolidate

---

### 🟢 LOW PRIORITY / MINOR

#### Issue #7: No Error Handling untuk Network
**File:** `dashboard_ui.py`
**Issue:** Jika koneksi internet mati, app bisa crash
```python
def _load_feed(self):
    if not hasattr(self, "tbl_feed"):
        return
    rows = list_published_news(limit=100)  # ❌ No try/catch
```

#### Issue #8: Hard-coded Intervals
**File:** `dashboard_ui.py`
```python
self.refresh_timer.start(10000)  # 10s
self.feed_timer.start(15000)     # 15s
self.hb_timer.start(20000)       # 20s
```
**Recommendation:** Make configurable

#### Issue #9: No Input Validation
**Example:** Username bisa pakai spasi, special chars
**Recommendation:** Add regex validation

---

## 🔧 RECOMMENDED FIXES (Priority Order)

### URGENT (Do First):
1. ✅ **Security:** Move `config.ini` to `.gitignore`, create template
2. ✅ **Security:** Rotate database password di Railway
3. ✅ Fix PyQt import inconsistency
4. ✅ Add try/catch untuk database operations

### IMPORTANT (Do Soon):
5. ✅ Cleanup redundant files (pilih 1 main file)
6. ✅ Add proper error handling
7. ✅ Update documentation (README)
8. ✅ Add logging untuk debugging

### NICE TO HAVE (Can Wait):
9. ⏳ Input validation improvements
10. ⏳ Configurable timers
11. ⏳ Unit tests

---

## 📝 TESTING SCRIPT

Saya akan buatkan script otomatis untuk test basic functionality:
- Connection test
- Login test
- Database operations test

---

## 🎯 NEXT STEPS

**Immediate Actions:**
1. Fix security issues (config.ini)
2. Test manual semua fitur yang ada
3. Implement error handling
4. Document findings

**Want me to:**
- [ ] Create `.gitignore` file?
- [ ] Create `config.ini.example` template?
- [ ] Fix PyQt import issues?
- [ ] Add comprehensive error handling?
- [ ] Create automated test script?
- [ ] Cleanup redundant files?

Pilih mana yang mau dikerjakan dulu! 🚀
