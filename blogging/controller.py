from blogging.blog import Blog
from blogging.post import Post
from datetime import datetime

class Controller:
    """
    Step 4: add post creation + read-only ops (search/retrieve/list).
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
        if self.current_blog is not None and self.current_blog.id == old_id:
            return False
        target = self.search_blog(old_id)
        if target is None:
            return False
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
        self.current_blog = None
        for b in self.blogs:
            if b.id == id:
                self.current_blog = b
                break

    def unset_current_blog(self):
        self.current_blog = None

    def get_current_blog(self):
        if not self.logged_in:
            return None
        return self.current_blog

    # ---------- POST READ OPS ----------
    def create_post(self, title, text):
        if not self.logged_in:
            return None
        if self.current_blog is None:
            return None
        now = datetime.now()
        p = Post(self.next_post_code, title, text, now, now)
        self.current_blog.add_post(p)
        self.next_post_code += 1
        return p

    def search_post(self, code):
        if not self.logged_in:
            return None
        if self.current_blog is None:
            return None
        return self.current_blog.get_post(code)

    def retrieve_posts(self, keyword):
        if not self.logged_in:
            return None
        if self.current_blog is None:
            return None
        return self.current_blog.retrieve_post(keyword)

    def list_posts(self):
        if not self.logged_in:
            return None
        if self.current_blog is None:
            return None
        # Blog.list_posts() already sorts newest-first by code
        return self.current_blog.list_posts()
