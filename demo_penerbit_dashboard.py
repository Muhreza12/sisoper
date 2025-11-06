# demo_penerbit_dashboard.py — Standalone Demo untuk Penerbit Dashboard
"""
Demo launcher untuk test penerbit dashboard tanpa perlu login
Langsung buka dashboard untuk lihat tampilan
"""

import sys
from PyQt5.QtWidgets import QApplication

def main():
    """Launch penerbit dashboard demo"""
    
    print("="*60)
    print("  🎨 PENERBIT DASHBOARD DEMO")
    print("="*60)
    print("\nLaunching beautiful penerbit dashboard...")
    print("Username: demo_penerbit")
    print("Session: Demo mode (no database required)")
    print("\n" + "="*60 + "\n")
    
    app = QApplication(sys.argv)
    
    try:
        from penerbit_dashboard import PenerbitDashboard
        
        # Create dashboard in demo mode
        dashboard = PenerbitDashboard(
            username="demo_penerbit",
            session_id=None  # No session in demo mode
        )
        
        # Show info message
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox(dashboard)
        msg.setWindowTitle("Demo Mode")
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            "🎨 Penerbit Dashboard Demo\n\n"
            "This is a demo mode to showcase the UI.\n\n"
            "⚠️ Features that require database:\n"
            "• Saving articles\n"
            "• Loading statistics\n"
            "• Loading article list\n\n"
            "✅ Features you can test:\n"
            "• UI/UX design\n"
            "• Text editor\n"
            "• Navigation\n"
            "• Dark theme\n"
            "• Animations"
        )
        msg.setStandardButtons(QMessageBox.Ok)
        
        # Show dashboard
        dashboard.show()
        
        # Show info after dashboard is visible
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(500, msg.exec_)
        
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\nMake sure these files exist:")
        print("• penerbit_dashboard.py")
        print("• app_db_fixed.py")
        print("\nAnd dependencies installed:")
        print("• pip install PyQt5")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
