from django.test import TestCase

from pf.models import Catagory, Blog, Message, User

from django.urls import reverse

# Create your tests here.
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

#Tests for viewing the list of created blogs
class BlogsViewTest(MyTestCase):
    def setUp(self):
        super(BlogsViewTest, self).setUp()

        for num in range(8):
            blog = Blog.objects.create(blogName='Blog #{0}'.format(num))
            blog.catagories.add(self.cat1)
            blog.catagories.add(self.cat2)
            blog.save

    #Test to ensure a user is not redirected if not logged in
    def test_no_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure an admin is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogs.html')

    #Test to ensure that the user sees 5 blogs on first page
    def test_list_5_blogs_1st_page(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['blogs']) == 5)

    #Test to ensure that the user sees 4 blogs on first page
    def test_list_4_blogs_2nd_page(self):
        response = self.client.get(reverse('blogs')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['blogs']) == 4)
