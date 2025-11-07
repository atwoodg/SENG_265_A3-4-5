import unittest
from blogging.blog import Blog
from blogging.post import Post
from datetime import datetime

#class to test blog class
class BlogTest(unittest.TestCase):

    def setUp(self):
        self.blog = Blog(1234, "Test Name", "test_url", "test@email")
        self.postA = Post(1, "Post A", "This is post A", datetime.now(), datetime.now())
        self.postB = Post(2, "Post B", "This is post B", datetime.now(), datetime.now())

    #Checks initialization is correct
    def test_blog_init(self):
        self.assertEqual(self.blog.id, 1234)
        self.assertEqual(self.blog.name, "Test Name")
        self.assertEqual(self.blog.url, "test_url")
        self.assertEqual(self.blog.email, "test@email")

    #Adds post to list of posts and ensures it was added and list is correct length
    def test_add_post(self):
        self.blog.add_post(self.postA)
        self.assertIn(self.postA, self.blog.posts)
        self.assertEqual(len(self.blog.posts), 1)

    #Adds post and checks if it can be retrieved by its code
    def test_get_post(self):
        self.blog.add_post(self.postA)
        retrieved_post = self.blog.get_post(1)
        self.assertEqual(retrieved_post, self.postA)

    #Adds post to list of posts and removes it, checks if list of posts is now empty
    def test_remove_post(self):
        empty_blog = []
        self.blog.add_post(self.postB)
        self.blog.remove_post(2)
        self.assertEqual(empty_blog, self.blog.posts)
        self.assertEqual(len(self.blog.posts), 0)

    #Adds two posts, retrieves posts containing 'post a', checks that only postA is retrieved
    def test_retrieve_post(self):
        self.blog.add_post(self.postA)
        self.blog.add_post(self.postB)
        retrieved = self.blog.retrieve_post("post a")
        self.assertEqual(retrieved, [self.postA])

    #Adds posts with codes 1,2 and verifies list_post method returns list in descending order
    def test_list_posts(self):
        order = [self.postB,self.postA]
        self.blog.add_post(self.postA)
        self.blog.add_post(self.postB)
        codes = self.blog.list_posts()
        self.assertEqual(order, codes)

    #Tests that eq verifies equality properly
    def test_eq(self):
        example_blog = Blog(1234, "Test Name", "test_url", "test@email")
        self.assertEqual(example_blog, self.blog)

    #Tests that __str__ output contains blog attributes
    def test_str(self):
        example_output = self.blog.__str__()
        self.assertIn("Test Name", example_output)
        self.assertIn("test_url", example_output)
        self.assertIn("test@email", example_output)
