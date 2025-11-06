# integrated_main_with_monitoring.py - Main file dengan Enhanced Admin Dashboard
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from db import init_db, connect, user_exists, create_user
from admin_dashboard import EnhancedAdminDashboard
from user_dashboard import UserDashboard
import sqlite3
import datetime

ACCENT = "#4F46E5"   # indigo
ACCENT_HOVER = "#4338CA"
DANGER = "#DC2626"
FG = "#0f172a"
MUTED = "#64748b"
BG = "#f1f5f9"
CARD = "#ffffff"

def apply_global_style(app):
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Segoe UI", 10))
    app.setStyleSheet(f"""
        QWidget {{
            color: {FG};
            background: {BG};
        }}
        QLineEdit {{
            height: 36px;
            padding: 6px 10px;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            background: #fff;
        }}
        QLineEdit:focus {{ border: 1px solid {ACCENT}; }}
        QLabel[role="muted"] {{ color: {MUTED}; }}
    """)

def make_card(parent):
    card = QtWidgets.QFrame(parent)
    card.setObjectName("card")
    card.setStyleSheet(f"""
        QFrame#card {{
            background: {CARD};
            border: 1px solid #e2e8f0;
            border-radius: 16px;
        }}
    """)
    effect = QtWidgets.QGraphicsDropShadowEffect(card)
    effect.setBlurRadius(24)
    effect.setColor(QtGui.QColor(15, 23, 42, 35))
    effect.setOffset(0, 12)
    card.setGraphicsEffect(effect)
    return card

def primary_button(text):
    btn = QtWidgets.QPushButton(text)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    btn.setStyleSheet(f"""
        QPushButton {{
            height: 40px; border-radius: 10px; border: none;
            background: {ACCENT}; color: white; font-weight: 600;
        }}
        QPushButton:hover {{ background: {ACCENT_HOVER}; }}
    """)
    return btn

def ghost_button(text):
    btn = QtWidgets.QPushButton(text)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    btn.setStyleSheet("""
        QPushButton {
            height: 40px; border-radius: 10px;
            background: transparent; border: 1px solid #e2e8f0;
            color: #0f172a; font-weight: 600;
        }
        QPushButton:hover { border-color: #4F46E5; color: #4F46E5; }
    """)
    return btn

def log_user_activity(username, action, details="", success=True):
    """Log user activity to monitoring database."""
    try:
        with sqlite3.connect("admin_monitoring.db") as conn:
            conn.execute("""
                INSERT INTO user_activities (username, action, details, success)
                VALUES (?, ?, ?, ?)
            """, (username, action, details, success))
    except Exception as e:
        print(f"Logging error: {e}")

class RegisterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Daftar Akun")
        self.resize(440, 360)

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)

        card = make_card(self)
        outer.addWidget(card)
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QtWidgets.QLabel("Buat Akun Baru")
        title.setStyleSheet("font-size: 20px; font-weight: 700;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QtWidgets.QLabel("Isi data di bawah dengan benar.")
        subtitle.setProperty("role", "muted")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(subtitle)

        form = QtWidgets.QFormLayout()
        form.setSpacing(10)
        self.username_edit = QtWidgets.QLineEdit(); self.username_edit.setPlaceholderText("mis. reza")
        self.password_edit = QtWidgets.QLineEdit(); self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password); self.password_edit.setPlaceholderText("min. 4 karakter")
        self.confirm_edit  = QtWidgets.QLineEdit(); self.confirm_edit.setEchoMode(QtWidgets.QLineEdit.Password); self.confirm_edit.setPlaceholderText("ulangi password")
        self.role_combo = QtWidgets.QComboBox(); self.role_combo.addItems(["user", "admin"])

        form.addRow("Username", self.username_edit)
        form.addRow("Password", self.password_edit)
        form.addRow("Konfirmasi", self.confirm_edit)
        form.addRow("Role", self.role_combo)
        layout.addLayout(form)

        # Toggle show password
        toggles = QtWidgets.QHBoxLayout()
        self.show_pw = QtWidgets.QCheckBox("Lihat password")
        self.show_pw.stateChanged.connect(self.toggle_password)
        toggles.addWidget(self.show_pw); toggles.addStretch(1)
        layout.addLayout(toggles)

        self.msg = QtWidgets.QLabel(""); self.msg.setStyleSheet(f"color:{DANGER};")
        layout.addWidget(self.msg)

        row = QtWidgets.QHBoxLayout()
        self.btn_daftar = primary_button("Daftar")
        self.btn_batal  = ghost_button("Batal")
        row.addWidget(self.btn_daftar); row.addWidget(self.btn_batal)
        layout.addLayout(row)

        self.btn_batal.clicked.connect(self.reject)
        self.btn_daftar.clicked.connect(self.handle_register)

    def toggle_password(self, state):
        mode = QtWidgets.QLineEdit.Normal if state == QtCore.Qt.Checked else QtWidgets.QLineEdit.Password
        self.password_edit.setEchoMode(mode)
        self.confirm_edit.setEchoMode(mode)

    def handle_register(self):
        u = self.username_edit.text().strip()
        p = self.password_edit.text().strip()
        c = self.confirm_edit.text().strip()
        role = self.role_combo.currentText()

        if not u or not p or not c:
            self.msg.setText("Semua field wajib diisi.")
            log_user_activity(u or "unknown", "REGISTRATION_FAILED", "Empty fields", False)
            return
        if len(u) < 3 or len(p) < 4:
            self.msg.setText("Username min 3, password min 4.")
            log_user_activity(u, "REGISTRATION_FAILED", "Username/password too short", False)
            return
        if p != c:
            self.msg.setText("Konfirmasi password tidak cocok.")
            log_user_activity(u, "REGISTRATION_FAILED", "Password confirmation mismatch", False)
            return
        if user_exists(u):
            self.msg.setText("Username sudah dipakai.")
            log_user_activity(u, "REGISTRATION_FAILED", "Username already exists", False)
            return

        try:
            create_user(u, p, role)
            log_user_activity(u, "USER_REGISTERED", f"Successfully registered with role: {role}", True)
        except Exception as e:
            self.msg.setText(f"Gagal membuat akun: {e}")
            log_user_activity(u, "REGISTRATION_ERROR", f"Registration failed: {str(e)}", False)
            return

        QtWidgets.QMessageBox.information(self, "Sukses", "Akun berhasil dibuat. Silakan login.")
        self.accept()

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Insight — Login with Enhanced Monitoring")
        self.resize(520, 420)

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(28, 28, 28, 28)
        outer.setSpacing(22)

        # Logo
        logo = QtWidgets.QLabel()
        try:
            pixmap = QtGui.QPixmap("logo.jpg")
            pixmap = pixmap.scaledToWidth(160, QtCore.Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
        except:
            logo.setText("🔐 LOGO")
            logo.setStyleSheet("font-size: 24px;")
        logo.setAlignment(QtCore.Qt.AlignCenter)
        outer.addWidget(logo)

        # Title
        header = QtWidgets.QLabel("🔐 Crypto Insight (Enhanced Monitoring)")
        header.setAlignment(QtCore.Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: 800;")
        outer.addWidget(header)

        subtitle = QtWidgets.QLabel("Masuk ke akun Anda untuk melanjutkan.")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        subtitle.setProperty("role", "muted")
        outer.addWidget(subtitle)

        card = make_card(self); card.setMaximumWidth(460)
        outer.addWidget(card, alignment=QtCore.Qt.AlignHCenter)

        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        form = QtWidgets.QFormLayout(); form.setSpacing(10)
        self.username_edit = QtWidgets.QLineEdit(); self.username_edit.setPlaceholderText("Username")
        self.password_edit = QtWidgets.QLineEdit(); self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        form.addRow("Username", self.username_edit)
        form.addRow("Password", self.password_edit)
        layout.addLayout(form)

        # Toggle show password
        toggle_row = QtWidgets.QHBoxLayout()
        self.show_pw = QtWidgets.QCheckBox("Lihat password")
        self.show_pw.stateChanged.connect(self.toggle_password)
        toggle_row.addWidget(self.show_pw); toggle_row.addStretch(1)
        layout.addLayout(toggle_row)

        self.msg = QtWidgets.QLabel(""); self.msg.setStyleSheet(f"color:{DANGER};")
        layout.addWidget(self.msg)

        btn_row = QtWidgets.QHBoxLayout()
        self.login_btn    = primary_button("Masuk")
        self.register_btn = ghost_button("Daftar Akun")
        self.exit_btn     = ghost_button("Keluar")
        btn_row.addWidget(self.login_btn)
        btn_row.addWidget(self.register_btn)
        btn_row.addWidget(self.exit_btn)
        layout.addLayout(btn_row)

        self.login_btn.clicked.connect(self.handle_login)
        self.register_btn.clicked.connect(self.open_register)
        self.exit_btn.clicked.connect(QtWidgets.qApp.quit)

        # Enable Enter key for login
        self.password_edit.returnPressed.connect(self.handle_login)

    def toggle_password(self, state):
        mode = QtWidgets.QLineEdit.Normal if state == QtCore.Qt.Checked else QtWidgets.QLineEdit.Password
        self.password_edit.setEchoMode(mode)

    def handle_login(self):
        u = self.username_edit.text().strip()
        p = self.password_edit.text().strip()

        if not u or not p:
            self.msg.setText("Username dan password wajib diisi.")
            log_user_activity(u or "unknown", "LOGIN_FAILED", "Empty credentials", False)
            return

        try:
            conn = connect(); cur = conn.cursor()
            cur.execute("SELECT username, password, role FROM users WHERE username = ?", (u,))
            row = cur.fetchone(); conn.close()
        except Exception as e:
            self.msg.setText(f"DB error: {e}")
            log_user_activity(u, "LOGIN_ERROR", f"Database error: {str(e)}", False)
            return

        if not row or row[1] != p:
            self.msg.setText("Username atau password salah.")
            failure_reason = "User not found" if not row else "Wrong password"
            log_user_activity(u, "LOGIN_FAILED", failure_reason, False)
            return

        # Successful login
        role = row[2]
        log_user_activity(u, "LOGIN_SUCCESS", f"Logged in with role: {role}", True)
        
        if role == "admin": 
            self.open_admin(u)
        else: 
            self.open_user(u)

    def open_register(self):
        log_user_activity("SYSTEM", "REGISTER_DIALOG_OPENED", "User opened registration dialog")
        dlg = RegisterDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            self.username_edit.setText(dlg.username_edit.text())
            self.password_edit.setFocus()
            self.msg.setText("Akun baru dibuat. Silakan login.")

    def open_admin(self, username):
        log_user_activity(username, "ADMIN_DASHBOARD_OPENED", "Admin dashboard accessed")
        self.admin = EnhancedAdminDashboard(username=username)
        self.admin.logout_btn.clicked.connect(lambda: self.back_to_login_from_admin(username))
        self.admin.show(); self.hide()

    def back_to_login_from_admin(self, username):
        log_user_activity(username, "ADMIN_LOGOUT", "Admin logged out from dashboard")
        self.admin.close()
        self.username_edit.clear(); self.password_edit.clear(); self.msg.clear(); self.show()

    def open_user(self, username):
        log_user_activity(username, "USER_DASHBOARD_OPENED", "User dashboard accessed")
        self.user = UserDashboard(username=username)
        self.user.logout_btn.clicked.connect(lambda: self.back_to_login_from_user(username))
        self.user.show(); self.hide()

    def back_to_login_from_user(self, username):
        log_user_activity(username, "USER_LOGOUT", "User logged out from dashboard")
        self.user.close()
        self.username_edit.clear(); self.password_edit.clear(); self.msg.clear(); self.show()

def main():
    # Initialize database
    init_db()
    
    app = QtWidgets.QApplication(sys.argv)
    apply_global_style(app)
    w = LoginWindow()
    w.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()