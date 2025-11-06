# main_beautiful.py — Launcher untuk Beautiful Auth UI
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPalette, QColor

def main():
    """Main entry point dengan beautiful UI"""
    app = QApplication(sys.argv)
    
    # Set dark palette
    pal = app.palette()
    pal.setColor(QPalette.Window, QColor("#0a0b0e"))
    pal.setColor(QPalette.WindowText, QColor("#e5e7eb"))
    pal.setColor(QPalette.Base, QColor("#15161d"))
    pal.setColor(QPalette.Text, QColor("#e5e7eb"))
    app.setPalette(pal)
    
    try:
        from auth_ui_beautiful import AuthWindow
        w = AuthWindow()
        w.show()
        sys.exit(app.exec_())
        
    except ImportError as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Import Error")
        msg.setText(f"Failed to import required modules:\n\n{str(e)}\n\n"
                   "Make sure all files are in the same folder:\n"
                   "- auth_ui_beautiful.py\n"
                   "- app_db_fixed.py\n"
                   "- modern_notification.py")
        msg.exec_()
        sys.exit(1)
        
    except Exception as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Application Error")
        msg.setText(f"An error occurred:\n\n{str(e)}")
        msg.exec_()
        sys.exit(1)

if __name__ == "__main__":
    main()
