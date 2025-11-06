# main_fixed.py — FIXED launcher with better error handling
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPalette, QColor

def main():
    """Main entry point with error handling"""
    app = QApplication(sys.argv)
    
    # Set dark palette
    pal = app.palette()
    pal.setColor(QPalette.Window, QColor("#0e0f12"))
    pal.setColor(QPalette.WindowText, QColor("#eaeaea"))
    pal.setColor(QPalette.Base, QColor("#0e0f12"))
    pal.setColor(QPalette.Text, QColor("#eaeaea"))
    app.setPalette(pal)
    
    try:
        # Import auth window
        from auth_ui_fixed import AuthWindow
        
        # Create and show window
        w = AuthWindow()
        w.show()
        
        # Run app
        sys.exit(app.exec_())
        
    except ImportError as e:
        # Show error if imports fail
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Import Error")
        msg.setText(f"Failed to import required modules:\n\n{str(e)}\n\n"
                   "Make sure all dependencies are installed:\n"
                   "pip install PyQt5 psycopg2-binary")
        msg.exec_()
        sys.exit(1)
        
    except Exception as e:
        # Catch any other errors
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Application Error")
        msg.setText(f"An error occurred:\n\n{str(e)}")
        msg.exec_()
        sys.exit(1)

if __name__ == "__main__":
    main()
