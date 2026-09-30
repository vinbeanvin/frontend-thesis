"""
models/user.py - User Model
============================
Defines the User class for authentication and session management.

Current: Simple class for session-based auth (no database).
Future: Extend with SQLAlchemy for database persistence,
        add password hashing with werkzeug.security.
"""


class User:
    """
    Represents a system user (admin) for authentication.
    
    Attributes:
        username (str): The user's login name.
        role (str): User role (e.g., 'admin').
    
    Future enhancements:
        - Add password_hash field with werkzeug.security
        - Add SQLAlchemy Column definitions
        - Inherit from Flask-Login's UserMixin
        - Add relationship to audit logs
    """
    
    def __init__(self, username, role='admin'):
        """
        Initialize a User instance.
        
        Args:
            username (str): The user's login name.
            role (str): The user's role. Defaults to 'admin'.
        """
        self.username = username
        self.role = role
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<User {self.username} ({self.role})>'
