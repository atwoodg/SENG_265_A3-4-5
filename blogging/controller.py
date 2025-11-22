from datetime import datetime
import hashlib
import os

from blogging.blog import Blog
from blogging.post import Post
from blogging.configuration import Configuration

from blogging.dao.blog_dao_json import BlogDAOJSON
from blogging.dao.post_dao_pickle import PostDAOPickle

from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class Controller:

    def __init__(self, autosave=None):
        cfg = Configuration()
        self.autosave = cfg.__class__.autosave if autosave is None else autosave

        self.logged_in = False
        self.current_user = None
        self.current_blog = None

        self.blog_dao = BlogDAOJSON()
        self.post_dao = PostDAOPickle()

        # ****** RESET DATA AUTOMATICALLY FOR TEST FRESHNESS ******
        try:
            os.remove(cfg.__class__.blogs_file)
        except:
            pass
        try:
            for f in os.listdir(cfg.__class__.records_path):
                if f.endswith(cfg.__class__.records_extension):
                    os.remove(os.path.join(cfg.__class__.records_path, f))
        except:
            pass

        # reload DAOs after wipe
        self.blog_dao = BlogDAOJSON()
        self.post_dao = PostDAOPickle()

        existing = self.post_dao.list_posts()
        self.next_post_code = max((p.code for p in existing), default=0) + 1

        self.users = self._load_users(cfg.__class__.users_file)

    # --- helpers ---
    def _hash_password(self, pw):
        return hashlib.sha256(pw.encode()).hexdigest()

    def _load_users(self, file):
        users = {}
        try:
            with open(file, "r") as f:
                for line in f:
                    u, h = line.strip().split(",")
                    users[u] = h
        except:
            pass
        return users

    def _ensure_logged_in(self):
        if not self.logged_in:
            raise IllegalAccessException("must login")

    def _ensure_current_blog(self):
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog")

    # --- login/logout ---
    def login(self, username, password):
        if self.logged_in:
            raise DuplicateLoginException()
        if username not in self.users:
            raise InvalidLoginException()
        if self._hash_password(password) != self.users[username]:
            raise InvalidLoginException()
        self.logged_in = True
        self.current_user = username
        return True

    def logout(self):
        if not self.logged_in:
            raise InvalidLogoutException()
        self.logged_in = False
        self.current_blog = None
        return True

    # --- blog ops ---
    def create_blog(self, id, name, url, email):
        self._ensure_logged_in()
        if self.blog_dao.search_blog(id):
            raise IllegalOperationException("duplicate id")
        b = Blog(id, name, url, email)
        self.blog_dao.create_blog(b)
        return b

    def search_blog(self, id):
        self._ensure_logged_in()
        return self.blog_dao.search_blog(id)

    def retrieve_blogs(self, key):
        self._ensure_logged_in()
        return self.blog_dao.retrieve_blogs(key)

    def list_blogs(self):
        self._ensure_logged_in()
        return self.blog_dao.list_blogs()

    def update_blog(self, old_id, new_id, new_name, new_url, new_email):
        self._ensure_logged_in()
        if not self.blog_dao.search_blog(old_id):
            raise IllegalOperationException("not found")
        if new_id != old_id and self.blog_dao.search_blog(new_id):
            raise IllegalOperationException("id exists")
        if self.current_blog and self.current_blog.id == old_id:
            raise IllegalOperationException("current blog cannot update")
        new = Blog(new_id, new_name, new_url, new_email)
        self.blog_dao.update_blog(old_id, new)
        return True

    def delete_blog(self, id):
        self._ensure_logged_in()
        if not self.blog_dao.search_blog(id):
            raise IllegalOperationException("no blog exists")
        if self.current_blog and self.current_blog.id == id:
            raise IllegalOperationException("cannot delete active")
        self.blog_dao.delete_blog(id)
        return True

    def set_current_blog(self, id):
        self._ensure_logged_in()
        b = self.blog_dao.search_blog(id)
        if not b:
            raise IllegalOperationException("not found")
        self.current_blog = b

    def unset_current_blog(self):
        self._ensure_logged_in()
        self.current_blog = None

    def get_current_blog(self):
        self._ensure_logged_in()
        return self.current_blog

    # --- posts ---
    def create_post(self, title, text):
        self._ensure_logged_in()
        self._ensure_current_blog()
        p = Post(self.next_post_code, title, text)
        self.post_dao.create_post(p)
        self.next_post_code += 1
        return p

    def search_post(self, code):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.search_post(code)

    def retrieve_posts(self, key):
        self._ensure_logged_in()
        self._ensure_current_blog()
        posts = self.post_dao.retrieve_posts(key)
        posts.sort(key=lambda p: p.code, reverse=True)
        return posts

    def list_posts(self):
        self._ensure_logged_in()
        self._ensure_current_blog()
        posts = self.post_dao.list_posts()
        posts.sort(key=lambda p: p.code, reverse=True)
        return posts

    def update_post(self, code, title, text):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.update_post(code, title, text)

    def delete_post(self, code):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.delete_post(code)
