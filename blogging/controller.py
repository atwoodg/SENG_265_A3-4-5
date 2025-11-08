from blogging.blog import Blog
from blogging.post import Post
from datetime import datetime

class Controller:
    """
    Step 3: update_blog, delete_blog, set_current_blog, unset_current_blog, get_current_blog.
    """

    def __init__(self):
        self.logged_in = False
        self.blogs = []
        self.current_blog = None
        self.next_post_code = 1

    # ---------- LOGIN / LOGOUT ----------
    def login(self, username, password):
        if self.logged_in:
            return False
        if username == "user" and password == "blogging2025":
            self.logged_in = True
            return True
        return False

    def logout(self):
        if not self.logged_in:
            return False
        self.logged_in = False
        self.current_blog = None
        return True

    # ---------- BLOG OPS ----------
    def create_blog(self, id, name, url, email):
        if not self.logged_in:
            return None
        for b in self.blogs:
            if b.id == id:
                return None
        blog = Blog(id, name, url, email)
        self.blogs.append(blog)
        return blog

    def search_blog(self, id):
        if not self.logged_in:
            return None
        for b in self.blogs:
            if b.id == id:
                return b
        return None

    def retrieve_blogs(self, keyword):
        if not self.logged_in:
            return None
        out = []
        kw = (keyword or "").lower()
        for b in self.blogs:
            if kw in b.name.lower():
                out.append(b)
        return out

    def list_blogs(self):
        if not self.logged_in:
            return None
        return list(self.blogs)

    def update_blog(self, old_id, new_id, new_name, new_url, new_email):
        if not self.logged_in:
            return False
        # cannot update the current blog; must unset first
        if self.current_blog is not None and self.current_blog.id == old_id:
            return False
        target = self.search_blog(old_id)
        if target is None:
            return False
        # new id must be either same or unused
        if new_id != old_id:
            for b in self.blogs:
                if b.id == new_id:
                    return False
        target.id = new_id
        target.name = new_name
        target.url = new_url
        target.email = new_email
        return True

    def delete_blog(self, id):
        if not self.logged_in:
            return False
        # cannot delete the current blog
        if self.current_blog is not None and self.current_blog.id == id:
            return False
        for i, b in enumerate(self.blogs):
            if b.id == id:
                del self.blogs[i]
                return True
        return False

    # ---------- CURRENT BLOG ----------
    def set_current_blog(self, id):
        if not self.logged_in:
            return
        found = None
        for b in self.blogs:
            if b.id == id:
                found = b
                break
        self.current_blog = found

    def unset_current_blog(self):
        self.current_blog = None

    def get_current_blog(self):
        if not self.logged_in:
            return None
        return self.current_blog
