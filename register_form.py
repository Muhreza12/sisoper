from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5 import QtGui
from db import user_exists, create_user

class RegisterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Daftar Akun Baru")
        self.setModal(True)
        self.resize(520, 360)
        self._build_ui()

    def _build_ui(self):
        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(18,18,18,18)

        card = QtWidgets.QWidget(objectName="Card")
        shadow = QGraphicsDropShadowEffect(blurRadius=24, xOffset=0, yOffset=8)
        shadow.setColor(QtGui.QColor(0,0,0,180))
        card.setGraphicsEffect(shadow)

        cl = QtWidgets.QVBoxLayout(card)
        cl.setContentsMargins(24,24,24,24)
        cl.setSpacing(12)

        title = QtWidgets.QLabel("Buat Akun", objectName="Title")
        title.setAlignment(QtCore.Qt.AlignCenter)
        subtitle = QtWidgets.QLabel("Isi data di bawah ini", objectName="Subtitle")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        cl.addWidget(title)
        cl.addWidget(subtitle)

        form = QtWidgets.QFormLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(12)

        self.username = QtWidgets.QLineEdit(placeholderText="Username")

        pw_row = QtWidgets.QHBoxLayout()
        self.password = QtWidgets.QLineEdit(placeholderText="Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_pw = QtWidgets.QToolButton(text="👁")
        self.btn_pw.setCheckable(True)
        self.btn_pw.toggled.connect(self._toggle_pw)
        pw_row.addWidget(self.password, 1)
        pw_row.addWidget(self.btn_pw, 0)
        pww = QtWidgets.QWidget(); pww.setLayout(pw_row)

        cf_row = QtWidgets.QHBoxLayout()
        self.confirm = QtWidgets.QLineEdit(placeholderText="Ulangi Password")
        self.confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_cf = QtWidgets.QToolButton(text="👁")
        self.btn_cf.setCheckable(True)
        self.btn_cf.toggled.connect(self._toggle_cf)
        cf_row.addWidget(self.confirm, 1)
        cf_row.addWidget(self.btn_cf, 0)
        cfw = QtWidgets.QWidget(); cfw.setLayout(cf_row)

        form.addRow("Username", self.username)
        form.addRow("Password", pww)
        form.addRow("Konfirmasi", cfw)
        cl.addLayout(form)

        self.msg = QtWidgets.QLabel(objectName="Error")
        cl.addWidget(self.msg)

        btns = QtWidgets.QHBoxLayout()
        self.btn_ok = QtWidgets.QPushButton("Daftar")
        self.btn_cancel = QtWidgets.QPushButton("Batal", objectName="Ghost")
        btns.addWidget(self.btn_ok, 3)
        btns.addWidget(self.btn_cancel, 2)
        cl.addLayout(btns)

        outer.addWidget(card)

        self.btn_ok.clicked.connect(self.handle_register)
        self.btn_cancel.clicked.connect(self.reject)
        self.confirm.returnPressed.connect(self.handle_register)

    def _toggle_pw(self, checked: bool):
        self.password.setEchoMode(QtWidgets.QLineEdit.Normal if checked else QtWidgets.QLineEdit.Password)

    def _toggle_cf(self, checked: bool):
        self.confirm.setEchoMode(QtWidgets.QLineEdit.Normal if checked else QtWidgets.QLineEdit.Password)

    def handle_register(self):
        u = self.username.text().strip().lower()
        p = self.password.text().strip()
        c = self.confirm.text().strip()

        if not u or not p or not c:
            self.msg.setText("Semua kolom wajib diisi.")
            return
        if len(u) < 3:
            self.msg.setText("Username minimal 3 karakter.")
            return
        if len(p) < 6:
            self.msg.setText("Password minimal 6 karakter.")
            return
        if p != c:
            self.msg.setText("Konfirmasi password tidak cocok.")
            return

        try:
            if user_exists(u):
                self.msg.setText("Username sudah terdaftar.")
                return
        except Exception as e:
            self.msg.setText(f"DB error (cek user): {e}")
            return

        try:
            ok = create_user(u, p, "user")
        except Exception as e:
            self.msg.setText(f"DB error (buat user): {e}")
            return

        if not ok:
            self.msg.setText("Gagal membuat user.")
            return

        QtWidgets.QMessageBox.information(self, "Sukses", f"Akun '{u}' berhasil dibuat.")
        self.accept()
