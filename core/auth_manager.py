"""
Authentication Manager
Handles user authentication with JSON file storage
"""
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import hashlib


class AuthManager:
    """Manages user authentication and registration"""
    
    def __init__(self, users_file='data/users.json'):
        self.users_file = users_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure users file exists"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)

        if not os.path.exists(self.users_file):
            # Create with default admin user using simple hash for compatibility
            default_users = {
                'admin': {
                    'id': 'admin',
                    'username': 'admin',
                    'password': 'admin123',  # Will be upgraded on first login
                    'email': 'admin@databoard.local',
                    'created_at': datetime.now().isoformat(),
                    'role': 'admin'
                }
            }
            self._save_users(default_users)
    
    def _load_users(self):
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _save_users(self, users):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        users = self._load_users()

        user = users.get(username)
        if user:
            stored_password = user['password']

            # Check 1: Direct plaintext match (for initial admin account)
            if stored_password == password:
                # Upgrade to hashed password
                try:
                    users[username]['password'] = generate_password_hash(password, method='pbkdf2:sha256')
                    self._save_users(users)
                except:
                    pass
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user.get('email', ''),
                    'role': user.get('role', 'user')
                }

            # Check 2: SHA256 hash match
            hashed = hashlib.sha256(password.encode()).hexdigest()
            if stored_password == hashed:
                # Upgrade to better hash
                try:
                    users[username]['password'] = generate_password_hash(password, method='pbkdf2:sha256')
                    self._save_users(users)
                except:
                    pass
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user.get('email', ''),
                    'role': user.get('role', 'user')
                }

            # Check 3: Werkzeug password hash
            try:
                if check_password_hash(stored_password, password):
                    return {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user.get('email', ''),
                        'role': user.get('role', 'user')
                    }
            except (ValueError, Exception):
                # Hash format not compatible
                pass

        return None
    
    def register(self, username, password, email=''):
        """Register a new user"""
        users = self._load_users()

        # Check if username already exists
        if username in users:
            return False, 'Username already exists'

        # Validate username
        if len(username) < 3:
            return False, 'Username must be at least 3 characters'

        if not username.isalnum():
            return False, 'Username must contain only letters and numbers'

        # Create new user
        user_id = hashlib.md5(f"{username}{datetime.now()}".encode()).hexdigest()[:16]

        # Use compatible password hashing
        try:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        except:
            # Fallback to simple hash
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

        users[username] = {
            'id': user_id,
            'username': username,
            'password': hashed_password,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'role': 'user'
        }

        self._save_users(users)

        return True, 'User registered successfully'
    
    def get_user(self, username):
        """Get user information (without password)"""
        users = self._load_users()
        user = users.get(username)
        
        if user:
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user.get('email', ''),
                'role': user.get('role', 'user'),
                'created_at': user.get('created_at')
            }
        
        return None
    
    def update_password(self, username, new_password):
        """Update user password"""
        users = self._load_users()

        if username not in users:
            return False, 'User not found'

        # Use compatible password hashing
        try:
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        except:
            # Fallback to simple hash
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        users[username]['password'] = hashed_password
        self._save_users(users)

        return True, 'Password updated successfully'
