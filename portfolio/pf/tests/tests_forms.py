from django.test import TestCase
from pf.forms import BlogForm

from pf.models import Catagory, Blog, Message, User

# initialize global variables for testing
class MyTestCase(TestCase):
    def setUp(self):
        #Users
        self.admin = User.objects.create_user(username="mike", password="example",
            email="admin@pf.com", is_staff=True, is_superuser=True)
        self.user = User.objects.create_user(username="notmike", password="example",
            email="user@pf.com", is_staff=False, is_superuser=False)

        #Catagories
        self.cat1 = Catagory.objects.create(catagoryName="Computer Science")
        self.cat2 = Catagory.objects.create(catagoryName="Web Development")
        self.cat3 = Catagory.objects.create(catagoryName="Coding")

        #Blogs
        self.blog = Blog.objects.create(blogName="Example Blog")
        self.blog.catagories.add(self.cat1)
        self.blog.catagories.add(self.cat2)
        self.blog.catagories.add(self.cat3)
        self.blog.save

        #Messages
        self.message = Message.objects.create(blog=self.blog, title="Test",
            content="This is a blog message")

# Tests for Blogs
class BlogFormTest(MyTestCase):
    #Test to ensure a admin can create a blog successfully
    def test_valid_blog_creation(self):
        user = self.admin
        blog_name = "My first blog"
        data = {'blogName': blog_name, 'catagories': [str(self.cat1.id), str(self.cat2.id)]}
        form = BlogForm(data)
        self.assertTrue(form.is_valid())
