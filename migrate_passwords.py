"""
Migrate old scrypt passwords to compatible format
"""
import json
from werkzeug.security import generate_password_hash

def migrate_passwords():
    print("=" * 60)
    print("Password Migration Tool")
    print("=" * 60)

    users_file = 'data/users.json'

    # Load users
    with open(users_file, 'r') as f:
        users = json.load(f)

    print(f"\n📋 Found {len(users)} users")

    migrated = []

    for username, user_data in users.items():
        password = user_data['password']

        # Check if it's a scrypt hash (incompatible)
        if password.startswith('scrypt:'):
            print(f"\n🔄 User '{username}' has incompatible scrypt hash")
            print(f"   This user will need to:")
            print(f"   1. Use password reset, OR")
            print(f"   2. Contact admin for new password")

            # Set to a random password they don't know
            # (forces them to reset)
            import secrets
            temp_password = secrets.token_urlsafe(32)
            user_data['password'] = generate_password_hash(temp_password, method='pbkdf2:sha256')
            user_data['needs_reset'] = True
            migrated.append(username)

        elif password.startswith('pbkdf2:'):
            print(f"✅ User '{username}' - already using compatible pbkdf2")

        elif len(password) < 100:  # Likely plaintext
            print(f"⚠️  User '{username}' - has plaintext password (will auto-upgrade on login)")

    # Special handling for admin - reset to known password
    if 'admin' in users:
        print(f"\n🔑 Resetting admin password to: admin123")
        users['admin']['password'] = 'admin123'  # Will upgrade on first login
        users['admin']['needs_reset'] = False

    # Save
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)

    print(f"\n" + "=" * 60)
    print(f"✅ Migration complete!")
    print(f"   - {len(migrated)} users need password reset")
    print(f"   - admin password reset to: admin123")
    print(f"=" * 60)

    if migrated:
        print(f"\n⚠️  Users needing reset: {', '.join(migrated)}")

if __name__ == '__main__':
    migrate_passwords()
