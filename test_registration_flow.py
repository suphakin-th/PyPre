"""
Test the actual registration and login flow
"""
from core.auth_manager import AuthManager
import json

def test_registration_flow():
    print("=" * 60)
    print("Testing ACTUAL Registration and Login Flow")
    print("=" * 60)

    auth = AuthManager()

    # Clear test user if exists
    users = auth._load_users()
    if 'newuser' in users:
        del users['newuser']
        auth._save_users(users)
        print("\n🧹 Cleared existing 'newuser'")

    # Test 1: Register a new user
    print("\n1️⃣ Registering new user 'newuser' with password 'mypass123'...")
    success, msg = auth.register('newuser', 'mypass123', 'new@example.com')
    print(f"   Registration: {success} - {msg}")

    # Check what was stored
    users = auth._load_users()
    if 'newuser' in users:
        stored_hash = users['newuser']['password']
        print(f"   Stored password hash: {stored_hash[:50]}...")
    else:
        print("   ❌ User not found in database!")
        return

    # Test 2: Try to login immediately with same password
    print("\n2️⃣ Attempting login with 'newuser' / 'mypass123'...")
    user = auth.authenticate('newuser', 'mypass123')
    if user:
        print(f"   ✅ Login successful!")
        print(f"   User ID: {user['id']}")
        print(f"   Username: {user['username']}")
        print(f"   Email: {user['email']}")
    else:
        print(f"   ❌ Login FAILED! This is the bug!")

        # Debug: Let's check what's happening
        print("\n🔍 Debug Information:")
        print(f"   Username exists: {'newuser' in users}")
        print(f"   Stored hash: {stored_hash}")

        # Try manual verification
        from werkzeug.security import check_password_hash
        import hashlib

        print(f"\n   Testing different verification methods:")

        # Method 1: Werkzeug check
        try:
            result = check_password_hash(stored_hash, 'mypass123')
            print(f"   1. check_password_hash: {result}")
        except Exception as e:
            print(f"   1. check_password_hash: ERROR - {e}")

        # Method 2: Plaintext
        result = (stored_hash == 'mypass123')
        print(f"   2. Plaintext match: {result}")

        # Method 3: SHA256
        sha_hash = hashlib.sha256('mypass123'.encode()).hexdigest()
        result = (stored_hash == sha_hash)
        print(f"   3. SHA256 match: {result}")

    # Test 3: Try with admin account
    print("\n3️⃣ Testing admin account (admin/admin123)...")
    user = auth.authenticate('admin', 'admin123')
    if user:
        print(f"   ✅ Admin login successful!")
    else:
        print(f"   ❌ Admin login FAILED!")

    print("\n" + "=" * 60)

if __name__ == '__main__':
    test_registration_flow()
