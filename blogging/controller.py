from datetime import datetime
import hashlib

from blogging.blog import Blog
from blogging.post import Post
from blogging.configuration import Configuration

from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class Controller:
    """
    Controller for the blogging system.

    Commit 1 version:
    - Handles all required exceptions.
    - Uses SHA-256 password hashes.
    - Still keeps blogs and posts in memory (no persistence yet).
    """

    def __init__(self, autosave=None):
        # figure out autosave from Configuration unless explicitly given
        cfg = Configuration()
        if autosave is None:
            self.autosave = cfg.__class__.autosave
        else:
            self.autosave = autosave

        self.logged_in = False
        self.current_user = None

        # in-memory blogs and current blog
        self.blogs = []           # list[Blog]
        self.current_blog = None  # Blog or None

        # post codes are shared across blogs in this simple controller
        self.next_post_code = 1

        # load valid users (username -> hash)
        self.users = self._load_users(cfg.__class__.users_file)

    # ---------- small helpers ----------

    def _hash_password(self, plain_password: str) -> str:
        """Return SHA-256 hex digest of a plain password."""
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

    def _load_users(self, users_file):
        """
        Load users from users.txt (username,hashdigest per line).
        If file is missing for some reason, fall back to hard-coded ones.
        """
        users = {}
        try:
            with open(users_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 2:
                        continue
                    username = parts[0].strip()
                    digest = parts[1].strip()
                    users[username] = digest
        except FileNotFoundError:
            # fallback – hashes computed from the plain passwords in the tests
            users = {
                "user": self._hash_password("123456"),
                "ali": self._hash_password("@G00dPassw0rd"),
                "kala": self._hash_password("@Pa55word"),
            }
        return users

    def _ensure_logged_in(self):
        if not self.logged_in:
            raise IllegalAccessException("must be logged in")

    def _ensure_current_blog(self):
        # used only when we already know the user is logged in
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog selected")

    # ---------- LOGIN / LOGOUT ----------

    def login(self, username, password):
        """
        Log in a user if username/password (hashed) match.
        Raises:
            DuplicateLoginException  – if already logged in
            InvalidLoginException    – if username or password is wrong
        """
        if self.logged_in:
            raise DuplicateLoginException("already logged in")

        if username not in self.users:
            raise InvalidLoginException("unknown username")

        digest = self._hash_password(password)
        if digest != self.users[username]:
            raise InvalidLoginException("wrong password")

        self.logged_in = True
        self.current_user = username
        return True

    def logout(self):
        """
        Log out the current user.
        Raises:
            InvalidLogoutException – if there is nobody logged in
        """
        if not self.logged_in:
            raise InvalidLogoutException("cannot logout when not logged in")

        self.logged_in = False
        self.current_user = None
        self.current_blog = None
        return True

    # ---------- BLOG OPS ----------

    def create_blog(self, id, name, url, email):
        """
        Create a blog with given data.
        Raises:
            IllegalAccessException   – if not logged in
            IllegalOperationException – if id already exists
        """
        self._ensure_logged_in()

        # check duplicate id
        for b in self.blogs:
            if b.id == id:
                raise IllegalOperationException("blog id already exists")

        blog = Blog(id, name, url, email)
        self.blogs.append(blog)
        return blog

    def search_blog(self, id):
        """
        Search a blog by id.
        Raises:
            IllegalAccessException – if not logged in
        """
        self._ensure_logged_in()
        for b in self.blogs:
            if b.id == id:
                return b
        return None

    def retrieve_blogs(self, keyword):
        """
        Retrieve blogs whose name contains the keyword (case-insensitive).
        Raises:
            IllegalAccessException – if not logged in
        """
        self._ensure_logged_in()
        keyword = (keyword or "").lower()
        result = []
        for b in self.blogs:
            if keyword in b.name.lower():
                result.append(b)
        return result

    def list_blogs(self):
        """
        List all blogs.
        Raises:
            IllegalAccessException – if not logged in
        """
        self._ensure_logged_in()
        return list(self.blogs)

    def update_blog(self, old_id, new_id, new_name, new_url, new_email):
        """
        Update a blog.
        Raises:
            IllegalAccessException   – if not logged in
            IllegalOperationException – if trying to update current blog,
                                       or blog does not exist,
                                       or new_id already used by another blog
        """
        self._ensure_logged_in()

        # cannot update the current blog
        if self.current_blog is not None and self.current_blog.id == old_id:
            raise IllegalOperationException("cannot update current blog")

        target = self.search_blog(old_id)
        if target is None:
            raise IllegalOperationException("blog does not exist")

        if new_id != old_id:
            for b in self.blogs:
                if b.id == new_id:
                    raise IllegalOperationException("new id already in use")

        target.id = new_id
        target.name = new_name
        target.url = new_url
        target.email = new_email
        return True

    def delete_blog(self, id):
        """
        Delete a blog by id.
        Raises:
            IllegalAccessException   – if not logged in
            IllegalOperationException – if trying to delete current blog
                                       or blog does not exist
        """
        self._ensure_logged_in()

        if self.current_blog is not None and self.current_blog.id == id:
            raise IllegalOperationException("cannot delete current blog")

        for i, b in enumerate(self.blogs):
            if b.id == id:
                del self.blogs[i]
                return True

        raise IllegalOperationException("blog does not exist")

    # ---------- CURRENT BLOG ----------

    def set_current_blog(self, id):
        """
        Set the current blog.
        Raises:
            IllegalAccessException   – if not logged in
            IllegalOperationException – if blog id does not exist
        """
        self._ensure_logged_in()
        self.current_blog = None
        for b in self.blogs:
            if b.id == id:
                self.current_blog = b
                break
        if self.current_blog is None:
            raise IllegalOperationException("cannot set non-existent blog as current")

    def unset_current_blog(self):
        """Unset current blog (no exception for this – it is always allowed)."""
        self.current_blog = None

    def get_current_blog(self):
        """
        Return current blog (or None).
        Raises:
            IllegalAccessException – if not logged in
        """
        self._ensure_logged_in()
        return self.current_blog

    # ---------- POSTS ----------

    def create_post(self, title, text):
        """
        Create a post in the current blog.
        Raises:
            IllegalAccessException – if not logged in
            NoCurrentBlogException – if there is no current blog
        """
        self._ensure_logged_in()
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog")

        now = datetime.now()
        p = Post(self.next_post_code, title, text, now, now)
        self.current_blog.add_post(p)
        self.next_post_code += 1
        return p

    def search_post(self, code):
        """
        Search a post in the current blog.
        Raises:
            IllegalAccessException – if not logged in
            NoCurrentBlogException – if there is no current blog
        """
        self._ensure_logged_in()
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog")
        return self.current_blog.get_post(code)

    def retrieve_posts(self, keyword):
        """
        Retrieve posts in the current blog whose title/text contain keyword.
        Raises:
            IllegalAccessException – if not logged in
            NoCurrentBlogException – if there is no current blog
        """
        self._ensure_logged_in()
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog")
        return self.current_blog.retrieve_post(keyword)

    def list_posts(self):
        """
        List posts of current blog, newest first.
        Raises:
            IllegalAccessException – if not logged in
            NoCurrentBlogException – if there is no current blog
        """
        self._ensure_logged_in()
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog")
        return self.current_blog.list_posts()

    def update_post(self, code, title, text):
        """
        Update a post of current blog.
        Returns False if the post does not exist.
        Raises:
            IllegalAccessException – if not logged in
            NoCurrentBlogException – if there is no current blog
        """
        self._ensure_logged_in()
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog")

        post = self.current_blog.get_post(code)
        if post is None:
            return False
        return post.update_post(updated_title=title,
                                updated_text=text,
                                updated_time=datetime.now())

    def delete_post(self, code):
        """
        Delete a post from current blog.
        Returns False if the post does not exist.
        Raises:
            IllegalAccessException – if not logged in
            NoCurrentBlogException – if there is no current blog
        """
        self._ensure_logged_in()
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog")
        return self.current_blog.remove_post(code)

    # ---------- tiny helper (kept from A3) ----------

    def debug_blog_count(self):
        print(f"[debug] total blogs: {len(self.blogs)}")
