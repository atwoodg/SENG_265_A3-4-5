import json
import os
from blogging.blog import Blog
from blogging.configuration import Configuration
from blogging.dao.blog_dao import BlogDAO


class BlogEncoder(json.JSONEncoder):
    """JSON encoder for Blog objects."""
    def default(self, obj):
        if isinstance(obj, Blog):
            return {
                "id": obj.id,
                "name": obj.name,
                "url": obj.url,
                "email": obj.email
            }
        return json.JSONEncoder.default(self, obj)


class BlogDecoder(json.JSONDecoder):
    """JSON decoder for Blog objects."""
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        if {"id", "name", "url", "email"} <= d.keys():
            return Blog(d["id"], d["name"], d["url"], d["email"])
        return d


class BlogDAOJSON(BlogDAO):

    def __init__(self):
        cfg = Configuration()
        self.file_path = cfg.__class__.blogs_file

        # ensure file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def _read_all(self):
        with open(self.file_path, "r") as f:
            return json.load(f, cls=BlogDecoder)

    def _write_all(self, blogs):
        with open(self.file_path, "w") as f:
            json.dump(blogs, f, cls=BlogEncoder, indent=2)

    # ---------- DAO interface methods ----------

    def search_blog(self, key):
        blogs = self._read_all()
        for b in blogs:
            if b.id == key:
                return b
        return None

    def create_blog(self, blog):
        blogs = self._read_all()
        blogs.append(blog)
        self._write_all(blogs)
        return True

    def retrieve_blogs(self, search_string):
        blogs = self._read_all()
        keyword = (search_string or "").lower()
        return [b for b in blogs if keyword in b.name.lower()]

    def update_blog(self, key, blog):
        blogs = self._read_all()
        for i, b in enumerate(blogs):
            if b.id == key:
                blogs[i] = blog
                self._write_all(blogs)
                return True
        return False

    def delete_blog(self, key):
        blogs = self._read_all()
        new_list = [b for b in blogs if b.id != key]
        if len(new_list) == len(blogs):
            return False
        self._write_all(new_list)
        return True

    def list_blogs(self):
        return self._read_all()
