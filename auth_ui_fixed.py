# auth_ui_fixed.py — Modern Auth (Login & Register) - FIXED VERSION
# - Standardized to PyQt5 only
# - Improved error handling
# - Better user feedback

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

# Backend (app_db_fixed)
from app_db_fixed import (
    verify_user, create_user, user_exists, setup_database,
    start_session, health_check
)

# Modern notification
from modern_notification import ModernNotification

APP_NAME = "Crypto Insight"

def _icon(path: str) -> QtGui.QIcon:
    """Load icon from path if exists"""
    return QtGui.QIcon(path) if os.path.exists(path) else QtGui.QIcon()

# ---------- Small Helpers ----------
class LineEdit(QtWidgets.QLineEdit):
    """LineEdit with Enter key signal"""
    enterPressed = QtCore.pyqtSignal()
    
    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        if e.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.enterPressed.emit()

class PillButton(QtWidgets.QPushButton):
    """Styled pill-shaped button"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setMinimumHeight(46)
        self.setObjectName("pillButton")

class LinkButton(QtWidgets.QPushButton):
    """Styled link button"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFlat(True)
        self.setObjectName("linkButton")

class HeaderLogo(QtWidgets.QWidget):
    """Header with logo and title"""
    def __init__(self, title=APP_NAME, parent=None):
        super().__init__(parent)
        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 24)
        
        avatar = QtWidgets.QLabel()
        avatar.setFixedSize(40, 40)
        avatar.setObjectName("avatarCircle")
        
        label = QtWidgets.QLabel(title)
        label.setObjectName("appTitle")
        
        lay.addWidget(avatar)
        lay.addWidget(label)
        lay.addStretch(1)

class AuthCard(QtWidgets.QFrame):
    """Card container for auth forms"""
    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumWidth(380)
        
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(28, 28, 28, 28)
        v.setSpacing(16)
        
        ttl = QtWidgets.QLabel(title)
        ttl.setObjectName("title")
        
        sub = QtWidgets.QLabel(subtitle)
        sub.setObjectName("subtitle")
        sub.setWordWrap(True)
        
        v.addWidget(ttl)
        v.addWidget(sub)
        
        self.form = QtWidgets.QFormLayout()
        self.form.setHorizontalSpacing(12)
        self.form.setVerticalSpacing(10)
        v.addLayout(self.form)
        
        self.btn = PillButton("Continue")
        v.addWidget(self.btn)
        
        self.switch = LinkButton("Create account")
        v.addWidget(self.switch, 0, QtCore.Qt.AlignHCenter)

# ---------- Main Window ----------
class AuthWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} • Sign in")
        self.setWindowIcon(_icon("icon.ico"))
        self.resize(960, 600)
        self.setObjectName("root")

        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # ===== Left hero =====
        hero = QtWidgets.QFrame()
        hero.setObjectName("hero")
        lv = QtWidgets.QVBoxLayout(hero)
        lv.setContentsMargins(48, 48, 48, 48)
        lv.setSpacing(0)
        lv.addWidget(HeaderLogo(), 0)
        
        heroTitle = QtWidgets.QLabel("Discover crypto insights\nin one glance.")
        heroTitle.setObjectName("heroTitle")
        heroTitle.setWordWrap(True)
        
        lv.addStretch(1)
        lv.addWidget(heroTitle)
        lv.addStretch(2)
        root.addWidget(hero, 1)

        # ===== Right panel =====
        right = QtWidgets.QFrame()
        right.setObjectName("right")
        rv = QtWidgets.QVBoxLayout(right)
        rv.setContentsMargins(48, 48, 48, 48)
        rv.setSpacing(16)

        # Segmented toggle
        top = QtWidgets.QHBoxLayout()
        top.setSpacing(8)
        
        self.btnLoginTab = QtWidgets.QPushButton("Sign in")
        self.btnLoginTab.setCheckable(True)
        
        self.btnRegisterTab = QtWidgets.QPushButton("Create account")
        self.btnRegisterTab.setCheckable(True)
        
        for b in (self.btnLoginTab, self.btnRegisterTab):
            b.setObjectName("segBtn")
            b.setCursor(QtCore.Qt.PointingHandCursor)
            b.setMinimumHeight(36)
        
        segWrap = QtWidgets.QFrame()
        segWrap.setObjectName("segWrap")
        segLay = QtWidgets.QHBoxLayout(segWrap)
        segLay.setContentsMargins(6, 6, 6, 6)
        segLay.setSpacing(6)
        segLay.addWidget(self.btnLoginTab)
        segLay.addWidget(self.btnRegisterTab)
        
        top.addStretch(1)
        top.addWidget(segWrap, 0)
        top.addStretch(1)
        rv.addLayout(top)

        # Stack
        self.stack = QtWidgets.QStackedWidget()
        rv.addStretch(1)
        rv.addWidget(self.stack, 0, QtCore.Qt.AlignHCenter)
        rv.addStretch(2)
        root.addWidget(right, 1)

        # ----- Login card -----
        self.loginCard = AuthCard("Welcome back", "Masuk untuk lanjut")
        
        self.le_user = LineEdit()
        self.le_user.setPlaceholderText("Username")
        
        self.le_pass = LineEdit()
        self.le_pass.setPlaceholderText("Password")
        self.le_pass.setEchoMode(QtWidgets.QLineEdit.Password)

        # Show/hide password (login)
        self.showPassLogin = QtWidgets.QCheckBox("Show password")
        self.showPassLogin.toggled.connect(
            lambda on: self.le_pass.setEchoMode(
                QtWidgets.QLineEdit.Normal if on else QtWidgets.QLineEdit.Password
            )
        )

        self.loginCard.form.addRow(self.le_user)
        self.loginCard.form.addRow(self.le_pass)
        self.loginCard.form.addRow(self.showPassLogin)
        self.loginCard.btn.setText("Sign in")
        self.loginCard.switch.setText("Create a new account")
        self.stack.addWidget(self.loginCard)

        # ----- Register card -----
        self.regCard = AuthCard("Create account", "Daftar untuk mulai menggunakan aplikasi")
        
        self.re_user = LineEdit()
        self.re_user.setPlaceholderText("Username")
        
        self.re_pass = LineEdit()
        self.re_pass.setPlaceholderText("Password")
        self.re_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.re_pass2 = LineEdit()
        self.re_pass2.setPlaceholderText("Confirm password")
        self.re_pass2.setEchoMode(QtWidgets.QLineEdit.Password)

        # Show/hide password (register)
        self.showPassReg = QtWidgets.QCheckBox("Show passwords")
        def _toggle_reg(on):
            mode = QtWidgets.QLineEdit.Normal if on else QtWidgets.QLineEdit.Password
            self.re_pass.setEchoMode(mode)
            self.re_pass2.setEchoMode(mode)
        self.showPassReg.toggled.connect(_toggle_reg)

        # Role selector
        self.re_role = QtWidgets.QComboBox()
        self.re_role.addItems(["user", "penerbit"])

        self.regCard.form.addRow(self.re_user)
        self.regCard.form.addRow(self.re_pass)
        self.regCard.form.addRow(self.re_pass2)
        self.regCard.form.addRow(QtWidgets.QLabel("Role"), self.re_role)
        self.regCard.form.addRow(self.showPassReg)
        self.regCard.btn.setText("Create account")
        self.regCard.switch.setText("Already have an account?")
        self.stack.addWidget(self.regCard)

        # Signals
        self.btnLoginTab.clicked.connect(lambda: self.switchPage(0))
        self.btnRegisterTab.clicked.connect(lambda: self.switchPage(1))
        self.loginCard.switch.clicked.connect(lambda: self.switchPage(1))
        self.regCard.switch.clicked.connect(lambda: self.switchPage(0))
        self.loginCard.btn.clicked.connect(self.on_login)
        self.regCard.btn.clicked.connect(self.on_register)
        self.le_user.enterPressed.connect(self.on_login)
        self.le_pass.enterPressed.connect(self.on_login)
        self.re_user.enterPressed.connect(self.on_register)
        self.re_pass.enterPressed.connect(self.on_register)
        self.re_pass2.enterPressed.connect(self.on_register)

        # Shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+1"), self, activated=lambda: self.switchPage(0))
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+2"), self, activated=lambda: self.switchPage(1))

        self._apply_qss()
        self.switchPage(0, immediate=True)

        # Init DB tables with health check
        self._init_database()

    def _init_database(self):
        """Initialize database with error handling"""
        try:
            # Check database health first
            if not health_check():
                self.show_error(
                    "Database Connection Failed",
                    "Tidak dapat terhubung ke database.\n\n"
                    "Pastikan:\n"
                    "• File config.ini ada dan berisi DATABASE_URL yang benar\n"
                    "• Koneksi internet aktif\n"
                    "• Credential database valid"
                )
                return
            
            # Setup tables
            if not setup_database():
                self.show_error(
                    "Database Setup Failed",
                    "Gagal membuat tabel database.\n"
                    "Periksa log untuk detail error."
                )
        except Exception as e:
            self.show_error("Database Error", f"Error saat inisialisasi database:\n{str(e)}")

    # -------- Logic --------
    def switchPage(self, index: int, immediate=False):
        """Switch between login and register pages"""
        self.stack.setCurrentIndex(index)
        self.btnLoginTab.setChecked(index == 0)
        self.btnRegisterTab.setChecked(index == 1)

    def toast(self, text: str, notification_type="info"):
        """Show modern notification"""
        if notification_type == "success":
            notif = ModernNotification.success(self, "Berhasil!", text)
        elif notification_type == "error":
            notif = ModernNotification.error(self, "Error", text)
        elif notification_type == "warning":
            notif = ModernNotification.warning(self, "Peringatan", text)
        else:
            notif = ModernNotification.info(self, "Info", text)
        notif.show_notification()

    def show_error(self, title: str, message: str):
        """Show error message"""
        m = QtWidgets.QMessageBox(self)
        m.setWindowTitle(title)
        m.setText(message)
        m.setIcon(QtWidgets.QMessageBox.Critical)
        m.exec_()

    def on_login(self):
        """Handle login attempt"""
        u = self.le_user.text().strip()
        p = self.le_pass.text()
        
        if not u or not p:
            return self.toast("Isi username dan password.", "warning")
        
        # Verify credentials
        role = verify_user(u, p)
        if role:
            # Start session
            sid = start_session(u)
            if sid is None:
                return self.show_error(
                    "Session Error",
                    "Tidak bisa membuat sesi online.\n"
                    "Periksa koneksi database."
                )
            
            # Open dashboard
            try:
                from dashboard_ui import DashboardWindow
            except ImportError as e:
                return self.show_error(
                    "Import Error",
                    f"Dashboard tidak ditemukan:\n{str(e)}"
                )
            
            self.hide()
            self.dashboard = DashboardWindow(u, role, sid)
            self.dashboard.destroyed.connect(self.show)
            self.dashboard.show()
        else:
            self.toast("Username atau password salah.", "error")

    def on_register(self):
        """Handle registration attempt"""
        u = self.re_user.text().strip()
        p1 = self.re_pass.text()
        p2 = self.re_pass2.text()
        role = self.re_role.currentText().strip().lower()
        
        # Validation
        if not u or not p1:
            return self.toast("Isi username & password.", "warning")
        
        if len(u) < 3:
            return self.toast("Username minimal 3 karakter.", "warning")
        
        if len(p1) < 4:
            return self.toast("Password minimal 4 karakter.", "warning")
        
        if p1 != p2:
            return self.toast("Konfirmasi password tidak cocok.", "error")
        
        if user_exists(u):
            return self.toast("Username sudah dipakai.", "error")
        
        # Create user
        ok = create_user(u, p1, role)
        if ok:
            self.toast(f"Akun '{u}' (role: {role}) berhasil dibuat!", "success")
            # Clear form dan switch ke login
            self.re_user.clear()
            self.re_pass.clear()
            self.re_pass2.clear()
            self.switchPage(0)
            # Isi username di login form
            self.le_user.setText(u)
            self.le_pass.setFocus()
        else:
            self.show_error(
                "Registration Failed",
                "Gagal membuat akun.\nPeriksa koneksi database."
            )

    # -------- Style --------
    def _apply_qss(self):
        """Apply stylesheet"""
        self.setStyleSheet("""
        #root { background: #0e0f12; }
        #hero {
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #151824, stop:1 #0e0f12);
        }
        #right { background:#0e0f12; }
        #appTitle { color:#eaeaea; font-size:18px; font-weight:600; }
        #avatarCircle { border-radius:20px; background:#7c5cff; }
        #heroTitle { color:#fafafa; font-size:40px; font-weight:800; }
        #card { background:#121218; border:1px solid #26263a; border-radius:20px; }
        #title { color:#f2f2f2; font-size:24px; font-weight:700; }
        #subtitle { color:#b6b8c3; font-size:13px; }
        QLineEdit {
            background:#0e0f12; color:#e6e6e6;
            border:1px solid #2a2a3d; border-radius:12px; padding:12px 14px;
        }
        QLineEdit:focus { border-color:#7c5cff; }
        QComboBox {
            background:#0e0f12; color:#e6e6e6;
            border:1px solid #2a2a3d; border-radius:12px; padding:8px 10px;
        }
        #pillButton { background:#7c5cff; color:white; border:none; border-radius:24px; font-weight:700; font-size:15px; }
        #pillButton:hover { background:#6a4cf7; }
        #pillButton:pressed { background:#5840e6; }
        #linkButton { color:#b9b9ff; text-decoration:underline; padding:6px 8px; border:none; }
        #segWrap { background:#121218; border:1px solid #26263a; border-radius:16px; }
        QPushButton#segBtn {
            background:transparent; color:#d9d9e3; border:none; padding:8px 14px; border-radius:12px; font-weight:600;
        }
        QPushButton#segBtn:checked { background:#7c5cff; color:white; }
        """)
        
        font = QtGui.QFont("Segoe UI")
        font.setPointSize(10)
        self.setFont(font)

# Standalone preview
def _run():
    app = QtWidgets.QApplication(sys.argv)
    w = AuthWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    _run()
