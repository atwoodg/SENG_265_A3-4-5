from blogging.blog import Blog
from blogging.post import Post
from datetime import datetime

class Controller:
    """
    Final step: tiny debug helper and comment polish.
    All tests should pass with this version.
    """

    def __init__(self):
        self.logged_in = False
        self.blogs = []           # list of Blog objects
        self.current_blog = None  # currently selected Blog (or None)
        self.next_post_code = 1   # increases every time we create a post

    # ---------- LOGIN / LOGOUT ----------
    def login(self, username, password):
        # Only accept this pair (per tests/spec)
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
        # prevent duplicate ids
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
        result = []
        kw = (keyword or "").lower()
        for b in self.blogs:
            if kw in b.name.lower():
                result.append(b)
        return result

    def list_blogs(self):
        if not self.logged_in:
            return None
        return list(self.blogs)

    def update_blog(self, old_id, new_id, new_name, new_url, new_email):
        if not self.logged_in:
            return False
        # cannot update the current blog
        if self.current_blog is not None and self.current_blog.id == old_id:
            return False
        target = self.search_blog(old_id)
        if target is None:
            return False
        # new id must be unused unless unchanged
        if new_id != old_id:
            for b in self.blogs:
                if b.id == new_id:
                    return False
        # apply changes
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

    # ---------- POSTS ----------
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
        # newest first (Blog.list_posts sorts by code desc)
        return self.current_blog.list_posts()

    def update_post(self, code, title, text):
        if not self.logged_in:
            return False
        if self.current_blog is None:
            return False
        post = self.current_blog.get_post(code)
        if post is None:
            return False
        return post.update_post(updated_title=title, updated_text=text, updated_time=datetime.now())

    def delete_post(self, code):
        if not self.logged_in:
            return False
        if self.current_blog is None:
            return False
        return self.current_blog.remove_post(code)

    # ---------- tiny helper ----------
    def debug_blog_count(self):
        # small helper used while testing locally
        print(f"[debug] total blogs: {len(self.blogs)}")
