from blogging.blog import Blog
from blogging.post import Post
from datetime import datetime

class Controller:

    #Initialization
    def __init__(self):
        self.logged_in = False
        self.blog = []
        self.current_blog = None


