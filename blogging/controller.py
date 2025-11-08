"""
controller.py
Controller class handles blog and post management.
"""

from blogging.blog import Blog
from blogging.post import Post
from datetime import datetime

class Controller:
    """Controls login, blog, and post interactions."""

    def __init__(self):
        """Initialize controller with no blogs and not logged in."""
        self.logged_in = False
        self.blog = []
        self.current_blog = None

    def login(self, user, password):
        """Logs a user in if credentials match."""
        if self.logged_in:
            return False
        if user == "user" and password == "blogging2025":
            self.logged_in = True
            return True
        return False
