"""Simple file-based authentication service for testing"""

import json
import os
import hashlib
from datetime import datetime

USERS_FILE = 'users.json'

class AuthService:
    """Handle user authentication with file storage"""
    
    def __init__(self):
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file if it doesn't exist"""
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'w') as f:
                json.dump({}, f)
    
    def _load_users(self):
        """Load users from file"""
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    
    def _save_users(self, users):
        """Save users to file"""
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def signup(self, first_name, last_name, email, password, newsletter=False):
        """Register a new user"""
        users = self._load_users()
        
        # Check if user already exists
        if email in users:
            return {'success': False, 'error': 'User already exists'}
        
        # Create new user
        users[email] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': self._hash_password(password),
            'newsletter': newsletter,
            'created_at': datetime.now().isoformat()
        }
        
        self._save_users(users)
        return {'success': True, 'message': 'User registered successfully'}
    
    def login(self, email, password):
        """Authenticate user"""
        users = self._load_users()
        
        if email not in users:
            return {'success': False, 'error': 'Invalid email or password'}
        
        user = users[email]
        
        if user['password'] != self._hash_password(password):
            return {'success': False, 'error': 'Invalid email or password'}
        
        return {
            'success': True,
            'user': {
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email']
            }
        }
    
    def get_user(self, email):
        """Get user information"""
        users = self._load_users()
        
        if email not in users:
            return None
        
        user = users[email]
        return {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email']
        }



