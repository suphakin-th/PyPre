"""
Test authentication system
"""
from core.auth_manager import AuthManager

def test_auth():
    print("=" * 60)
    print("Testing Authentication System")
    print("=" * 60)

    auth = AuthManager()

    # Test 1: Authenticate admin
    print("\n1. Testing admin login with 'admin123'...")
    user = auth.authenticate('admin', 'admin123')
    if user:
        print(f"   ✅ Success! User: {user['username']}, Role: {user['role']}")
    else:
        print(f"   ❌ Failed! Authentication returned None")

    # Test 2: Wrong password
    print("\n2. Testing with wrong password...")
    user = auth.authenticate('admin', 'wrongpass')
    if user:
        print(f"   ❌ Should have failed but succeeded!")
    else:
        print(f"   ✅ Correctly rejected wrong password")

    # Test 3: Register new user
    print("\n3. Testing user registration...")
    success, msg = auth.register('testuser', 'testpass123', 'test@example.com')
    if success:
        print(f"   ✅ Registration successful: {msg}")

        # Try to login with new user
        print("\n4. Testing login with new user...")
        user = auth.authenticate('testuser', 'testpass123')
        if user:
            print(f"   ✅ New user login successful! User: {user['username']}")
        else:
            print(f"   ❌ New user login failed!")
    else:
        print(f"   ❌ Registration failed: {msg}")

    # Test 4: Check password after update
    print("\n5. Checking if admin password was auto-upgraded...")
    import json
    with open('data/users.json', 'r') as f:
        users = json.load(f)
        admin_pass = users['admin']['password']
        if admin_pass == 'admin123':
            print(f"   ⚠️  Password still in plaintext (will upgrade on next login)")
        else:
            print(f"   ✅ Password is hashed: {admin_pass[:20]}...")

    print("\n" + "=" * 60)
    print("Authentication test complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_auth()
