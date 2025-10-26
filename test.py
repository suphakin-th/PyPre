#!/usr/bin/env python3
"""
DataBoard - Test Script
Quick verification that all components are working
"""

import os
import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from flask import Flask
        print("  ✓ Flask imported successfully")
        
        import pandas as pd
        print("  ✓ Pandas imported successfully")
        
        from werkzeug.security import generate_password_hash
        print("  ✓ Werkzeug imported successfully")
        
        from core.data_processor import DataProcessor
        print("  ✓ DataProcessor imported successfully")
        
        from core.auth_manager import AuthManager
        print("  ✓ AuthManager imported successfully")
        
        from core.chart_builder import ChartBuilder
        print("  ✓ ChartBuilder imported successfully")
        
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

def test_directories():
    """Test that required directories exist or can be created"""
    print("\nTesting directories...")
    dirs = ['data', 'data/uploads', 'data/datasets', 'data/dashboards', 'static', 'templates', 'core']
    
    all_exist = True
    for directory in dirs:
        if os.path.exists(directory):
            print(f"  ✓ {directory} exists")
        else:
            print(f"  ✗ {directory} does not exist")
            all_exist = False
    
    return all_exist

def test_files():
    """Test that required files exist"""
    print("\nTesting files...")
    files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'templates/login.html',
        'templates/dashboard.html',
        'static/dashboard.js',
        'core/__init__.py',
        'core/auth_manager.py',
        'core/data_processor.py',
        'core/chart_builder.py'
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"  ✓ {file} exists")
        else:
            print(f"  ✗ {file} does not exist")
            all_exist = False
    
    return all_exist

def test_auth_manager():
    """Test authentication manager"""
    print("\nTesting AuthManager...")
    try:
        from core.auth_manager import AuthManager
        
        # Initialize
        auth = AuthManager('data/test_users.json')
        
        # Test registration
        success, msg = auth.register('testuser', 'testpass123', 'test@example.com')
        if success:
            print(f"  ✓ User registration works: {msg}")
        else:
            print(f"  ✗ User registration failed: {msg}")
            return False
        
        # Test authentication
        user = auth.authenticate('testuser', 'testpass123')
        if user:
            print(f"  ✓ User authentication works")
        else:
            print(f"  ✗ User authentication failed")
            return False
        
        # Cleanup
        if os.path.exists('data/test_users.json'):
            os.remove('data/test_users.json')
        
        return True
    except Exception as e:
        print(f"  ✗ AuthManager test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("DataBoard - Component Test Suite")
    print("="*60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Directories", test_directories()))
    results.append(("Files", test_files()))
    results.append(("AuthManager", test_auth_manager()))
    
    print("\n" + "="*60)
    print("Test Results:")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:20s}: {status}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✅ All tests passed! DataBoard is ready to run.")
        print("\nTo start the server, run:")
        print("  python app.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
