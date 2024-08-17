from django.test import TestCase
from django.contrib.auth import get_user_model
from Blog.models import Blog_table
import datetime
User = get_user_model()

class BlogTableModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.blog = Blog_table.objects.create(
            user_id=self.user,
            title='Test Blog Title',
            Description='This is a test description',
            image='path/to/test_image.jpg'
        )

    def test_blog_table_creation(self):
        """
        Ensure that a Blog_table instance is created with the correct values.
        """
        self.assertEqual(self.blog.user_id.email, 'testuser@gmail.com')
        self.assertEqual(self.blog.title, 'Test Blog Title')
        self.assertEqual(self.blog.Description, 'This is a test description')
        self.assertEqual(self.blog.image, 'path/to/test_image.jpg')
        self.assertIsNotNone(self.blog.date)  # date should be automatically set

    def test_blog_table_string_representation(self):
        """
        Ensure the string representation of the Blog_table instance is correct.
        """
        expected_string_representation = self.blog.title
        self.assertEqual(str(self.blog), expected_string_representation)

    def test_blog_table_user_relationship(self):
        """
        Ensure that the Blog_table instance is correctly linked to a User instance.
        """
        self.assertEqual(self.blog.user_id, self.user)

    def test_default_image(self):
        """
        Ensure that the Blog_table instance has a default image if no image is provided.
        """
        blog_without_image = Blog_table.objects.create(
            user_id=self.user,
            title='Blog without image',
            Description='This blog has no image provided',
        )
        self.assertEqual(blog_without_image.image, '')

    def test_title_max_length(self):
        """
        Ensure that the 'title' field's max length is 150 characters.
        """
        max_length = self.blog._meta.get_field('title').max_length
        self.assertEqual(max_length, 150)

    def test_blog_table_field_types(self):
        self.assertIsInstance(self.blog.user_id, User)
        self.assertIsInstance(self.blog.title, str)
        self.assertIsInstance(self.blog.Description, str)
        self.assertIsInstance(self.blog.date, datetime.datetime)

    def test_blog_table_date_auto_now_add(self):
        self.assertIsNotNone(self.blog.date)
