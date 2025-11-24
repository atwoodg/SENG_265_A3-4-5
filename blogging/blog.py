class Blog:

    def __init__(self, id, name, url, email):
        self.id = id
        self.name = name
        self.url = url
        self.email = email
        self.posts = []


    def add_post(self, post):
        self.posts.append(post)
        return True

    def get_post(self, code):
        for p in self.posts:
            if p.code == code:
                return p
        return None

    def list_posts(self):
        return sorted(self.posts, key=lambda p: p.code, reverse=True)

    def remove_post(self, code):
        before = len(self.posts)
        self.posts = [p for p in self.posts if p.code != code]
        return len(self.posts) != before

    def retrieve_post(self, key):
        key = key.lower()
        return [p for p in self.posts if key in p.title.lower() or key in p.text.lower()]

    def __str__(self):
        return f"Blog ID: {self.id}\nName: {self.name}\nURL: {self.url}\nEmail: {self.email}"

    def __eq__(self, other):
        return isinstance(other, Blog) and \
               self.id == other.id and \
               self.name == other.name and \
               self.url == other.url and \
               self.email == other.email
