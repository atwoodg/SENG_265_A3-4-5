from blogging import post

class Blog:

    #Initializing blog object attributes
    def __init__(self, id, name, url, email):
        self.id = id
        self.name = name
        self.url = url
        self.email = email
        self.posts = []

    #Method to add post to list of posts in blog
    def add_post(self, new_post):
        self.posts.append(new_post)

    #Method that retrieves a certain code from a blog based on posts code
    def get_post(self, code):
        for p in self.posts:
            if p.code == code:
                return p
        return None

    #Removes post from blog based on posts code
    def remove_post(self, code):
        for p in self.posts:
            if p.code == code:
                self.posts.remove(p)
                return True
        return False

    #Returns posts that contain any instance of keyword in title or text
    def retrieve_post(self, keyword):
        contains = []
        for p in self.posts:
            if keyword.lower() in p.title.lower() or keyword.lower() in p.text.lower():
                contains.append(p)
        return contains

    #Sorts posts in newest order
    def list_posts(self):
        self.posts.sort(reverse=True)
        return self.posts

    #Output blog
    def __str__(self):
        return f"Blog ID: {self.id}\nName: {self.name}\nURL: {self.url}\nEmail: {self.email}"

    #Tests equality of attributes
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return(self.id == other.id and
                   self.name == other.name and
                   self.url == other.url and
                   self.email == other.email)
        else:
            return False

