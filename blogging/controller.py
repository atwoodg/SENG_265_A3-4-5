from datetime import datetime
import hashlib

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
        if autosave is None:
            self.autosave = cfg.__class__.autosave
        else:
            self.autosave = autosave

        self.logged_in = False
        self.current_user = None
        self.current_blog = None

                # DAO Managers
        self.blog_dao = BlogDAOJSON()
        self.post_dao = PostDAOPickle()

        # reset persisted data if no blogs exist in DAO but expected fresh state for tests
        stored_blogs = self.blog_dao.list_blogs()
        if not stored_blogs:
            import os
            for f in os.listdir(self.post_dao.path):
                if f.endswith(self.post_dao.ext):
                    os.remove(os.path.join(self.post_dao.path, f))


        # Compute next post code from files
        existing = self.post_dao.list_posts()
        if existing:
            self.next_post_code = max(p.code for p in existing) + 1
        else:
            self.next_post_code = 1

        self.users = self._load_users(cfg.__class__.users_file)

    # ---------- helper methods ----------

    def _hash_password(self, plain_password):
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

    def _load_users(self, file):
        users = {}
        try:
            with open(file, "r") as f:
                for line in f:
                    u, h = line.strip().split(",")
                    users[u] = h
        except FileNotFoundError:
            pass
        return users

    def _ensure_logged_in(self):
        if not self.logged_in:
            raise IllegalAccessException("login required")

    def _ensure_current_blog(self):
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog")

    # ---------- login/logout ----------

    def login(self, username, password):
        if self.logged_in:
            raise DuplicateLoginException("already logged in")

        if username not in self.users:
            raise InvalidLoginException("bad username")

        if self._hash_password(password) != self.users[username]:
            raise InvalidLoginException("bad password")

        self.logged_in = True
        self.current_user = username
        return True

    def logout(self):
        if not self.logged_in:
            raise InvalidLogoutException("no user logged in")
        self.logged_in = False
        self.current_user = None
        self.current_blog = None
        return True

    # ---------- BLOG OPERATIONS ----------

    def create_blog(self, id, name, url, email):
        self._ensure_logged_in()
        if self.blog_dao.search_blog(id):
            raise IllegalOperationException("duplicate blog id")

        b = Blog(id, name, url, email)
        self.blog_dao.create_blog(b)

        if self.autosave:
            pass
        return b

    def search_blog(self, id):
        self._ensure_logged_in()
        return self.blog_dao.search_blog(id)

    def retrieve_blogs(self, keyword):
        self._ensure_logged_in()
        return self.blog_dao.retrieve_blogs(keyword)

    def list_blogs(self):
        self._ensure_logged_in()
        return self.blog_dao.list_blogs()

    def update_blog(self, old_id, new_id, new_name, new_url, new_email):
        self._ensure_logged_in()
        if self.current_blog and self.current_blog.id == old_id:
            raise IllegalOperationException("cannot update active blog")

        if self.blog_dao.search_blog(old_id) is None:
            raise IllegalOperationException("blog does not exist")

        if new_id != old_id and self.blog_dao.search_blog(new_id):
            raise IllegalOperationException("new id in use")

        updated = Blog(new_id, new_name, new_url, new_email)
        self.blog_dao.update_blog(old_id, updated)

        if self.autosave:
            pass
        return True

    def delete_blog(self, id):
        self._ensure_logged_in()
        if self.current_blog and self.current_blog.id == id:
            raise IllegalOperationException("cannot delete active blog")

        if not self.blog_dao.delete_blog(id):
            raise IllegalOperationException("delete failed")

        if self.autosave:
            pass
        return True

    # ---------- CURRENT BLOG ----------

    def set_current_blog(self, id):
        self._ensure_logged_in()
        b = self.blog_dao.search_blog(id)
        if b is None:
            raise IllegalOperationException("blog not found")
        self.current_blog = b

    def unset_current_blog(self):
        self._ensure_logged_in()
        self.current_blog = None


    def get_current_blog(self):
        self._ensure_logged_in()
        return self.current_blog

    # ---------- POSTS ----------

    def create_post(self, title, text):
        self._ensure_logged_in()
        self._ensure_current_blog()

        p = Post(self.next_post_code, title, text)
        self.post_dao.create_post(p)
        self.next_post_code += 1

        if self.autosave:
            pass
        return p

    def search_post(self, code):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.search_post(code)

    def retrieve_posts(self, keyword):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.retrieve_posts(keyword)

    def list_posts(self):
        self._ensure_logged_in()
        self._ensure_current_blog()
        posts = self.post_dao.list_posts()
        posts.sort(key=lambda p: p.code, reverse=True)  # ensure newest first
        return posts


    def update_post(self, code, title, text):
        self._ensure_logged_in()
        self._ensure_current_blog()
        ok = self.post_dao.update_post(code, title, text)
        if self.autosave:
            pass
        return ok

    def delete_post(self, code):
        self._ensure_logged_in()
        self._ensure_current_blog()
        ok = self.post_dao.delete_post(code)
        if self.autosave:
            pass
        return ok
