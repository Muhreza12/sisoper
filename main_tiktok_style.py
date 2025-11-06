# main_tiktok_style.py — Launcher (Disederhanakan untuk Kamus Manual)
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer

# =================================================================
# KELAS SPLASH SCREEN (Teks di-hardcode)
# =================================================================
class SplashScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.setFixedSize(400, 570) 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setObjectName("mainFrame")
        
        layout = QtWidgets.QVBoxLayout(self.main_frame)
        layout.setContentsMargins(40, 50, 40, 50) 
        layout.setSpacing(20)

        # --- Logo ---
        logo_layout = QtWidgets.QHBoxLayout()
        logo_circle = QtWidgets.QLabel()
        logo_circle.setFixedSize(32, 32) 
        logo_circle.setObjectName("logoCircle")
        
        logo_text = QtWidgets.QLabel("Crypto Insight")
        logo_text.setObjectName("logoText")
        
        logo_layout.addWidget(logo_circle)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()

        # --- Teks Utama (Hardcode) ---
        self.title = QtWidgets.QLabel("Discover crypto insights in one glance.")
        self.title.setObjectName("titleText")
        self.title.setWordWrap(True)

        layout.addLayout(logo_layout)
        layout.addStretch(1) 
        layout.addWidget(self.title)
        layout.addStretch(2) 

        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.addWidget(self.main_frame)
        
        # Terapkan Stylesheet
        self.setStyleSheet("""
            #mainFrame {
                background-color: #111827; /* Dark background */
                border-radius: 15px;
            }
            #logoCircle {
                background-color: #8B5CF6; /* Purple */
                border-radius: 16px; /* 32 / 2 */
            }
            #logoText {
                color: white;
                font-size: 18px;
                font-weight: 600;
                padding-left: 5px;
            }
            #titleText {
                color: white;
                font-size: 42px;
                font-weight: 700;
                line-height: 40px;
            }
        """)

# =================================================================
# FUNGSI MAIN (YANG DIMODIFIKASI)
# =================================================================
def main():
    """Launch Splash Screen, then TikTok-style auth UI"""
    
    app = QtWidgets.QApplication(sys.argv)
    
    try:
        from auth_ui_tiktok_style import TikTokAuthWindow
        
        # 1. Buat Splash Screen
        splash = SplashScreen()
        
        # 2. Posisikan di tengah layar
        screen_geo = QtWidgets.QApplication.desktop().screenGeometry()
        center_pos = screen_geo.center() - splash.rect().center()
        splash.move(center_pos)
        
        # 3. Tampilkan Splash Screen
        splash.show()
        
        # 4. Buat Window Login (TIDAK PERLU translator lagi)
        main_window = TikTokAuthWindow()
        
        # 5. Buat fungsi untuk menukar window
        def show_main_window():
            splash.close()
            main_window.show()

        # 6. Set timer 2.5 detik untuk ganti ke main window
        QTimer.singleShot(2500, show_main_window) # 2500 ms = 2.5 detik
        
        sys.exit(app.exec_())
        
    except ImportError as e:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle("Import Error")
        msg.setText(f"Failed to import:\n\n{str(e)}\n\n"
                   "Required files:\n"
                   "- auth_ui_tiktok_style.py\n"
                   "- app_db_fixed.py\n"
                   "- modern_notification.py")
        msg.exec_()
        sys.exit(1)
        
    except Exception as e:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(f"An error occurred:\n\n{str(e)}")
        msg.exec_()
        sys.exit(1)

if __name__ == "__main__":
    main()