# auth_ui_beautiful.py — Beautiful Auth with Smooth Transitions & Animations
"""
Modern authentication UI dengan:
- Smooth slide transitions antara login/register
- Beautiful animations
- Input focus effects
- Loading indicators
- Success/error animations
"""

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup

# Backend
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


# ========== ANIMATED WIDGETS ==========

class AnimatedLineEdit(QtWidgets.QLineEdit):
    """LineEdit with floating label animation"""
    enterPressed = QtCore.pyqtSignal()
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self._placeholder = placeholder
        
    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        if e.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.enterPressed.emit()
    
    def focusInEvent(self, event):
        """Animate on focus"""
        super().focusInEvent(event)
        self.setStyleSheet("""
            AnimatedLineEdit {
                background:#0e0f12; color:#e6e6e6;
                border:2px solid #7c5cff; border-radius:12px; 
                padding:12px 14px; font-size:14px;
            }
        """)
    
    def focusOutEvent(self, event):
        """Remove animation on blur"""
        super().focusOutEvent(event)
        self.setStyleSheet("""
            AnimatedLineEdit {
                background:#0e0f12; color:#e6e6e6;
                border:1px solid #2a2a3d; border-radius:12px; 
                padding:12px 14px; font-size:14px;
            }
        """)


class AnimatedButton(QtWidgets.QPushButton):
    """Button with hover animation and loading state"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setMinimumHeight(48)
        self._loading = False
        self._original_text = text
        
        # Loading timer for animation
        self.loading_timer = QtCore.QTimer(self)
        self.loading_timer.timeout.connect(self._update_loading)
        self.loading_dots = 0
        
    def setLoading(self, loading):
        """Set loading state"""
        self._loading = loading
        if loading:
            self.setEnabled(False)
            self.loading_dots = 0
            self.loading_timer.start(300)
        else:
            self.loading_timer.stop()
            self.setText(self._original_text)
            self.setEnabled(True)
    
    def _update_loading(self):
        """Update loading animation"""
        dots = "." * (self.loading_dots % 4)
        self.setText(f"Loading{dots}")
        self.loading_dots += 1
    
    def enterEvent(self, event):
        """Scale up on hover"""
        if not self._loading:
            self.setCursor(QtCore.Qt.PointingHandCursor)


class SlidingStackedWidget(QtWidgets.QStackedWidget):
    """Stacked widget with slide animation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current = 0
        
    def slideToIndex(self, index):
        """Slide to specific index with animation"""
        if index == self.currentIndex():
            return
        
        direction = 1 if index > self.currentIndex() else -1
        
        # Get widgets
        current_widget = self.currentWidget()
        next_widget = self.widget(index)
        
        if not current_widget or not next_widget:
            self.setCurrentIndex(index)
            return
        
        # Setup positions
        width = self.width()
        next_widget.setGeometry(0, 0, width, self.height())
        next_widget.move(width * direction, 0)
        next_widget.show()
        next_widget.raise_()
        
        # Animations
        anim_current = QPropertyAnimation(current_widget, b"pos")
        anim_current.setDuration(400)
        anim_current.setStartValue(QtCore.QPoint(0, 0))
        anim_current.setEndValue(QtCore.QPoint(-width * direction, 0))
        anim_current.setEasingCurve(QEasingCurve.OutCubic)
        
        anim_next = QPropertyAnimation(next_widget, b"pos")
        anim_next.setDuration(400)
        anim_next.setStartValue(QtCore.QPoint(width * direction, 0))
        anim_next.setEndValue(QtCore.QPoint(0, 0))
        anim_next.setEasingCurve(QEasingCurve.OutCubic)
        
        # Parallel animation
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(anim_current)
        self.animation_group.addAnimation(anim_next)
        self.animation_group.finished.connect(lambda: self._animation_finished(index))
        
        self.animation_group.start()
    
    def _animation_finished(self, index):
        """Cleanup after animation"""
        self.setCurrentIndex(index)


# ========== MAIN AUTH WINDOW ==========

class AuthWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} • Sign in")
        self.setWindowIcon(_icon("icon.ico"))
        self.resize(960, 600)
        self.setObjectName("root")

        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # ===== Left hero panel =====
        hero = QtWidgets.QFrame()
        hero.setObjectName("hero")
        lv = QtWidgets.QVBoxLayout(hero)
        lv.setContentsMargins(48, 48, 48, 48)
        lv.setSpacing(0)
        
        # Logo
        logo_container = QtWidgets.QWidget()
        logo_layout = QtWidgets.QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 24)
        
        avatar = QtWidgets.QLabel()
        avatar.setFixedSize(48, 48)
        avatar.setObjectName("avatarCircle")
        avatar.setText("🔐")
        avatar.setAlignment(QtCore.Qt.AlignCenter)
        
        brand = QtWidgets.QLabel(APP_NAME)
        brand.setObjectName("brandName")
        
        logo_layout.addWidget(avatar)
        logo_layout.addWidget(brand)
        logo_layout.addStretch()
        
        lv.addWidget(logo_container)
        
        # Hero content
        heroTitle = QtWidgets.QLabel("Discover crypto\ninsights\nin one glance.")
        heroTitle.setObjectName("heroTitle")
        heroTitle.setWordWrap(True)
        
        heroSub = QtWidgets.QLabel("Track prices, manage portfolio,\nand stay updated with crypto news.")
        heroSub.setObjectName("heroSubtitle")
        heroSub.setWordWrap(True)
        
        lv.addStretch(1)
        lv.addWidget(heroTitle)
        lv.addSpacing(16)
        lv.addWidget(heroSub)
        lv.addStretch(2)
        
        root.addWidget(hero, 1)

        # ===== Right form panel =====
        right = QtWidgets.QFrame()
        right.setObjectName("right")
        rv = QtWidgets.QVBoxLayout(right)
        rv.setContentsMargins(48, 48, 48, 48)
        rv.setSpacing(20)

        # Tab toggle (modern segmented control)
        tab_container = QtWidgets.QWidget()
        tab_container.setObjectName("tabContainer")
        tab_layout = QtWidgets.QHBoxLayout(tab_container)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        
        self.btnLoginTab = QtWidgets.QPushButton("Sign in")
        self.btnLoginTab.setCheckable(True)
        self.btnLoginTab.setObjectName("tabBtn")
        self.btnLoginTab.setCursor(QtCore.Qt.PointingHandCursor)
        
        self.btnRegisterTab = QtWidgets.QPushButton("Create account")
        self.btnRegisterTab.setCheckable(True)
        self.btnRegisterTab.setObjectName("tabBtn")
        self.btnRegisterTab.setCursor(QtCore.Qt.PointingHandCursor)
        
        tab_layout.addWidget(self.btnLoginTab)
        tab_layout.addWidget(self.btnRegisterTab)
        
        rv.addWidget(tab_container, 0, QtCore.Qt.AlignCenter)
        rv.addSpacing(20)

        # Sliding stack for forms
        self.stack = SlidingStackedWidget()
        rv.addWidget(self.stack, 1)

        # ===== LOGIN FORM =====
        login_widget = QtWidgets.QWidget()
        login_layout = QtWidgets.QVBoxLayout(login_widget)
        login_layout.setSpacing(20)
        login_layout.setContentsMargins(0, 0, 0, 0)
        
        login_title = QtWidgets.QLabel("Welcome back")
        login_title.setObjectName("formTitle")
        login_title.setAlignment(QtCore.Qt.AlignCenter)
        
        login_subtitle = QtWidgets.QLabel("Sign in to continue")
        login_subtitle.setObjectName("formSubtitle")
        login_subtitle.setAlignment(QtCore.Qt.AlignCenter)
        
        login_layout.addWidget(login_title)
        login_layout.addWidget(login_subtitle)
        login_layout.addSpacing(10)
        
        # Login inputs
        self.le_user = AnimatedLineEdit("Username")
        self.le_pass = AnimatedLineEdit("Password")
        self.le_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Show password
        self.show_pass_login = QtWidgets.QCheckBox("Show password")
        self.show_pass_login.setObjectName("checkBox")
        self.show_pass_login.toggled.connect(
            lambda on: self.le_pass.setEchoMode(
                QtWidgets.QLineEdit.Normal if on else QtWidgets.QLineEdit.Password
            )
        )
        
        login_layout.addWidget(self.le_user)
        login_layout.addWidget(self.le_pass)
        login_layout.addWidget(self.show_pass_login)
        login_layout.addSpacing(10)
        
        # Login button
        self.btn_login = AnimatedButton("Sign in")
        self.btn_login.setObjectName("primaryBtn")
        login_layout.addWidget(self.btn_login)
        
        login_layout.addStretch()
        self.stack.addWidget(login_widget)

        # ===== REGISTER FORM =====
        register_widget = QtWidgets.QWidget()
        register_layout = QtWidgets.QVBoxLayout(register_widget)
        register_layout.setSpacing(16)
        register_layout.setContentsMargins(0, 0, 0, 0)
        
        register_title = QtWidgets.QLabel("Create account")
        register_title.setObjectName("formTitle")
        register_title.setAlignment(QtCore.Qt.AlignCenter)
        
        register_subtitle = QtWidgets.QLabel("Join us today")
        register_subtitle.setObjectName("formSubtitle")
        register_subtitle.setAlignment(QtCore.Qt.AlignCenter)
        
        register_layout.addWidget(register_title)
        register_layout.addWidget(register_subtitle)
        register_layout.addSpacing(10)
        
        # Register inputs
        self.re_user = AnimatedLineEdit("Username")
        self.re_pass = AnimatedLineEdit("Password")
        self.re_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.re_pass2 = AnimatedLineEdit("Confirm password")
        self.re_pass2.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Role selector
        role_container = QtWidgets.QWidget()
        role_layout = QtWidgets.QHBoxLayout(role_container)
        role_layout.setContentsMargins(0, 0, 0, 0)
        role_label = QtWidgets.QLabel("Role:")
        role_label.setObjectName("roleLabel")
        self.re_role = QtWidgets.QComboBox()
        self.re_role.addItems(["user", "penerbit"])
        self.re_role.setObjectName("comboBox")
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.re_role, 1)
        
        # Show passwords
        self.show_pass_reg = QtWidgets.QCheckBox("Show passwords")
        self.show_pass_reg.setObjectName("checkBox")
        def _toggle_reg(on):
            mode = QtWidgets.QLineEdit.Normal if on else QtWidgets.QLineEdit.Password
            self.re_pass.setEchoMode(mode)
            self.re_pass2.setEchoMode(mode)
        self.show_pass_reg.toggled.connect(_toggle_reg)
        
        register_layout.addWidget(self.re_user)
        register_layout.addWidget(self.re_pass)
        register_layout.addWidget(self.re_pass2)
        register_layout.addWidget(role_container)
        register_layout.addWidget(self.show_pass_reg)
        register_layout.addSpacing(10)
        
        # Register button
        self.btn_register = AnimatedButton("Create account")
        self.btn_register.setObjectName("primaryBtn")
        register_layout.addWidget(self.btn_register)
        
        register_layout.addStretch()
        self.stack.addWidget(register_widget)

        root.addWidget(right, 1)

        # ===== SIGNALS =====
        self.btnLoginTab.clicked.connect(lambda: self.switchPage(0))
        self.btnRegisterTab.clicked.connect(lambda: self.switchPage(1))
        self.btn_login.clicked.connect(self.on_login)
        self.btn_register.clicked.connect(self.on_register)
        self.le_user.enterPressed.connect(self.on_login)
        self.le_pass.enterPressed.connect(self.on_login)
        self.re_user.enterPressed.connect(self.on_register)
        self.re_pass.enterPressed.connect(self.on_register)
        self.re_pass2.enterPressed.connect(self.on_register)

        # Shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+1"), self, activated=lambda: self.switchPage(0))
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+2"), self, activated=lambda: self.switchPage(1))

        self._apply_style()
        self.switchPage(0)
        self._init_database()

    def _init_database(self):
        """Initialize database with error handling"""
        try:
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
            setup_database()
        except Exception as e:
            self.show_error("Database Error", f"Error saat inisialisasi database:\n{str(e)}")

    def switchPage(self, index: int):
        """Switch between login and register with animation"""
        self.stack.slideToIndex(index)
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
        """Handle login with loading animation"""
        u = self.le_user.text().strip()
        p = self.le_pass.text()
        
        if not u or not p:
            return self.toast("Isi username dan password.", "warning")
        
        # Show loading
        self.btn_login.setLoading(True)
        
        # Simulate async with QTimer (biar ada animasi loading)
        QtCore.QTimer.singleShot(500, lambda: self._do_login(u, p))
    
    def _do_login(self, u, p):
        """Actual login logic"""
        role = verify_user(u, p)
        self.btn_login.setLoading(False)
        
        if role:
            sid = start_session(u)
            if sid is None:
                return self.show_error(
                    "Session Error",
                    "Tidak bisa membuat sesi online.\nPeriksa koneksi database."
                )
            
            try:
                from dashboard_ui import DashboardWindow
            except ImportError as e:
                return self.show_error("Import Error", f"Dashboard tidak ditemukan:\n{str(e)}")
            
            self.hide()
            self.dashboard = DashboardWindow(u, role, sid)
            self.dashboard.destroyed.connect(self.show)
            self.dashboard.show()
        else:
            self.toast("Username atau password salah.", "error")

    def on_register(self):
        """Handle registration with loading animation"""
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
        
        # Show loading
        self.btn_register.setLoading(True)
        
        # Simulate async
        QtCore.QTimer.singleShot(500, lambda: self._do_register(u, p1, role))
    
    def _do_register(self, u, p1, role):
        """Actual registration logic"""
        ok = create_user(u, p1, role)
        self.btn_register.setLoading(False)
        
        if ok:
            self.toast(f"Akun '{u}' (role: {role}) berhasil dibuat!", "success")
            self.re_user.clear()
            self.re_pass.clear()
            self.re_pass2.clear()
            self.switchPage(0)
            self.le_user.setText(u)
            self.le_pass.setFocus()
        else:
            self.show_error("Registration Failed", "Gagal membuat akun.\nPeriksa koneksi database.")

    def _apply_style(self):
        """Apply beautiful stylesheet"""
        self.setStyleSheet("""
            /* Global */
            #root { background: #0a0b0e; }
            
            /* Hero Panel */
            #hero {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1b26, stop:1 #0a0b0e
                );
            }
            #avatarCircle {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7c5cff, stop:1 #6a4cf7
                );
                border-radius: 24px;
                font-size: 24px;
            }
            #brandName {
                color: #f0f0f0;
                font-size: 20px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            #heroTitle {
                color: #ffffff;
                font-size: 48px;
                font-weight: 800;
                line-height: 1.2;
                letter-spacing: -1px;
            }
            #heroSubtitle {
                color: #9ca3af;
                font-size: 16px;
                line-height: 1.6;
            }
            
            /* Right Panel */
            #right { background: #0a0b0e; }
            
            /* Tab Container */
            #tabContainer {
                background: #15161d;
                border: 1px solid #25262f;
                border-radius: 14px;
                padding: 6px;
                max-width: 380px;
            }
            QPushButton#tabBtn {
                background: transparent;
                color: #9ca3af;
                border: none;
                border-radius: 10px;
                padding: 12px 28px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton#tabBtn:checked {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7c5cff, stop:1 #6a4cf7
                );
                color: white;
            }
            QPushButton#tabBtn:hover:!checked {
                background: #1f2029;
                color: #d1d5db;
            }
            
            /* Form */
            #formTitle {
                color: #f9fafb;
                font-size: 28px;
                font-weight: 700;
            }
            #formSubtitle {
                color: #9ca3af;
                font-size: 14px;
            }
            
            /* Inputs */
            AnimatedLineEdit {
                background: #15161d;
                color: #e5e7eb;
                border: 1px solid #25262f;
                border-radius: 12px;
                padding: 14px 16px;
                font-size: 14px;
            }
            AnimatedLineEdit:focus {
                border: 2px solid #7c5cff;
                background: #1a1b26;
            }
            
            /* ComboBox */
            QComboBox#comboBox {
                background: #15161d;
                color: #e5e7eb;
                border: 1px solid #25262f;
                border-radius: 12px;
                padding: 12px 14px;
                font-size: 14px;
            }
            QComboBox#comboBox:focus {
                border: 2px solid #7c5cff;
            }
            QComboBox#comboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox#comboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #9ca3af;
                margin-right: 8px;
            }
            QComboBox#comboBox QAbstractItemView {
                background: #15161d;
                color: #e5e7eb;
                border: 1px solid #25262f;
                selection-background-color: #7c5cff;
                selection-color: white;
                padding: 4px;
            }
            
            /* Labels */
            #roleLabel {
                color: #9ca3af;
                font-size: 14px;
                font-weight: 500;
            }
            
            /* Checkbox */
            QCheckBox#checkBox {
                color: #9ca3af;
                font-size: 13px;
                spacing: 8px;
            }
            QCheckBox#checkBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #25262f;
                border-radius: 5px;
                background: #15161d;
            }
            QCheckBox#checkBox::indicator:checked {
                background: #7c5cff;
                border-color: #7c5cff;
                image: none;
            }
            QCheckBox#checkBox::indicator:checked:after {
                content: "✓";
                color: white;
            }
            
            /* Primary Button */
            QPushButton#primaryBtn {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7c5cff, stop:1 #6a4cf7
                );
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px;
                font-weight: 700;
                font-size: 15px;
                min-height: 48px;
            }
            QPushButton#primaryBtn:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #8b6cff, stop:1 #7a5cf7
                );
            }
            QPushButton#primaryBtn:pressed {
                background: #5840e6;
            }
            QPushButton#primaryBtn:disabled {
                background: #25262f;
                color: #6b7280;
            }
        """)
        
        font = QtGui.QFont("Segoe UI")
        font.setPointSize(10)
        self.setFont(font)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = AuthWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
