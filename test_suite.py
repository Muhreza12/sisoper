# test_suite.py — Automated Testing for Crypto Insight
"""
Automated testing script untuk Crypto Insight project
Run: python test_suite.py
"""

import sys
import os

# Test results storage
test_results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_test(name, status, message=""):
    """Print test result"""
    symbols = {'PASS': '✅', 'FAIL': '❌', 'WARN': '⚠️'}
    symbol = symbols.get(status, '•')
    print(f"{symbol} {name}: {status}")
    if message:
        print(f"   → {message}")
    
    if status == 'PASS':
        test_results['passed'].append(name)
    elif status == 'FAIL':
        test_results['failed'].append(name)
    else:
        test_results['warnings'].append(name)

def test_python_version():
    """Test Python version"""
    print_header("Testing Python Environment")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print_test("Python Version", "PASS", f"Python {version.major}.{version.minor}.{version.micro}")
    else:
        print_test("Python Version", "FAIL", f"Python {version.major}.{version.minor} (need 3.7+)")

def test_dependencies():
    """Test required dependencies"""
    print_header("Testing Dependencies")
    
    # PyQt5
    try:
        import PyQt5
        print_test("PyQt5", "PASS", f"Version {PyQt5.QtCore.PYQT_VERSION_STR}")
    except ImportError:
        print_test("PyQt5", "FAIL", "Not installed. Run: pip install PyQt5")
    
    # psycopg2
    try:
        import psycopg2
        print_test("psycopg2", "PASS", "Installed")
    except ImportError:
        print_test("psycopg2", "FAIL", "Not installed. Run: pip install psycopg2-binary")
    
    # configparser (built-in)
    try:
        import configparser
        print_test("configparser", "PASS", "Built-in module")
    except ImportError:
        print_test("configparser", "FAIL", "Missing built-in module")

def test_project_structure():
    """Test project file structure"""
    print_header("Testing Project Structure")
    
    required_files = [
        ('main.py', 'Main entry point'),
        ('auth_ui.py', 'Authentication UI'),
        ('dashboard_ui.py', 'Dashboard UI'),
        ('app_db.py', 'Database module'),
        ('requirements.txt', 'Dependencies list')
    ]
    
    optional_files = [
        ('config.ini', 'Database configuration'),
        ('README.md', 'Documentation'),
        ('.gitignore', 'Git ignore file')
    ]
    
    for filename, description in required_files:
        if os.path.exists(filename):
            print_test(f"{filename}", "PASS", description)
        else:
            print_test(f"{filename}", "FAIL", f"Missing: {description}")
    
    for filename, description in optional_files:
        if os.path.exists(filename):
            print_test(f"{filename}", "PASS", description)
        else:
            print_test(f"{filename}", "WARN", f"Optional: {description}")

def test_database_config():
    """Test database configuration"""
    print_header("Testing Database Configuration")
    
    # Check config.ini
    if os.path.exists('config.ini'):
        print_test("config.ini exists", "PASS", "Configuration file found")
        
        # Check if it has DATABASE_URL
        try:
            import configparser
            cfg = configparser.ConfigParser()
            cfg.read('config.ini', encoding='utf-8-sig')
            
            if 'server' in cfg and 'DATABASE_URL' in cfg['server']:
                url = cfg['server']['DATABASE_URL']
                if url.startswith('postgresql://'):
                    if 'USERNAME:PASSWORD@HOST' in url:
                        print_test("DATABASE_URL", "WARN", "Still using template values")
                    else:
                        print_test("DATABASE_URL", "PASS", "Configured")
                else:
                    print_test("DATABASE_URL", "FAIL", "Invalid format")
            else:
                print_test("DATABASE_URL", "FAIL", "Not found in config.ini")
        except Exception as e:
            print_test("config.ini parsing", "FAIL", str(e))
    else:
        print_test("config.ini", "WARN", "File not found (will use env var)")

def test_database_connection():
    """Test actual database connection"""
    print_header("Testing Database Connection")
    
    try:
        from app_db import connect, health_check
        
        # Test connection
        if health_check():
            print_test("Database Connection", "PASS", "Successfully connected to database")
        else:
            print_test("Database Connection", "FAIL", "Cannot connect to database")
            return
        
        # Test table creation
        from app_db import setup_database
        if setup_database():
            print_test("Database Setup", "PASS", "Tables created/verified")
        else:
            print_test("Database Setup", "FAIL", "Cannot setup tables")
            
    except ImportError:
        print_test("Database Module", "FAIL", "Cannot import app_db module")
    except Exception as e:
        print_test("Database Test", "FAIL", str(e))

def test_security():
    """Test security issues"""
    print_header("Testing Security")
    
    # Check if .gitignore exists and contains sensitive files
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            content = f.read()
        
        sensitive_patterns = ['config.ini', '.env', '*.db']
        for pattern in sensitive_patterns:
            if pattern in content:
                print_test(f"Ignore {pattern}", "PASS", "Protected from git")
            else:
                print_test(f"Ignore {pattern}", "WARN", f"Should add '{pattern}' to .gitignore")
    else:
        print_test(".gitignore", "WARN", "File not found - create one!")
    
    # Check if config.ini.example exists
    if os.path.exists('config.ini.example'):
        print_test("config.ini.example", "PASS", "Template exists")
    else:
        print_test("config.ini.example", "WARN", "Should create template")

def test_code_imports():
    """Test if main modules can be imported"""
    print_header("Testing Code Imports")
    
    modules = [
        ('app_db', 'Database module'),
        ('auth_ui', 'Authentication UI'),
        ('dashboard_ui', 'Dashboard UI')
    ]
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print_test(f"Import {module_name}", "PASS", description)
        except ImportError as e:
            print_test(f"Import {module_name}", "FAIL", str(e))
        except Exception as e:
            print_test(f"Import {module_name}", "WARN", f"Import error: {str(e)}")

def print_summary():
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    total = len(test_results['passed']) + len(test_results['failed']) + len(test_results['warnings'])
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed:   {len(test_results['passed'])}")
    print(f"❌ Failed:   {len(test_results['failed'])}")
    print(f"⚠️  Warnings: {len(test_results['warnings'])}")
    
    if test_results['failed']:
        print("\n❌ FAILED TESTS:")
        for test in test_results['failed']:
            print(f"   • {test}")
    
    if test_results['warnings']:
        print("\n⚠️  WARNINGS:")
        for test in test_results['warnings']:
            print(f"   • {test}")
    
    if not test_results['failed']:
        print("\n🎉 All critical tests passed!")
    else:
        print("\n⚠️  Some tests failed. Please fix before deployment.")
    
    print("\n" + "="*60 + "\n")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🔍 CRYPTO INSIGHT - AUTOMATED TEST SUITE".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Run all tests
    test_python_version()
    test_dependencies()
    test_project_structure()
    test_database_config()
    test_security()
    
    # These tests require working dependencies
    if 'PyQt5' in str(test_results['passed']):
        test_code_imports()
    
    # Database test (optional - might fail if config not set)
    try:
        test_database_connection()
    except:
        print_test("Database Connection", "WARN", "Skipped (config not ready)")
    
    # Print summary
    print_summary()

if __name__ == "__main__":
    main()
