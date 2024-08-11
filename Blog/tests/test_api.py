from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from Blog.models import Blog_table
from PIL import Image
import io
from Blog.serializers import BlogSerializer

class BlogAPITestCase(APITestCase):

    # def setUp(self):
    #     self.user = User.objects.create_user(username='testuser', password='testpassword')
    #     self.client = APIClient()
    #     self.client.force_authenticate(user=self.user)

    #     # Create an initial blog entry
    #     self.blog = Blog_table.objects.create(
    #         user_id=self.user,
    #         title='Test Blog Title',
    #         Description='Test Blog Description',
    #         image=self.generate_test_image_file()
    #     )
        
    #     self.blog_url = reverse('blogdetailapiview_name', kwargs={'pk': self.blog.pk})
    #     self.blogs_url = reverse('bloglistcreateapiview_name')

    def setUp(self):
        self.login_api_url = reverse('token_obtain_pair')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.data = {
            'username': "testuser",
            'password': "testpassword"
        }
        self.client = APIClient()
        self.response = self.client.post(self.login_api_url, self.data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.response.data['access']))

        # Create an initial blog entry
        self.blog = Blog_table.objects.create(
            user_id=self.user,
            title='Test Blog Title',
            Description='Test Blog Description',
            image=self.generate_test_image_file()
        )

        self.blog_url = reverse('blogdetailapiview_name', kwargs={'pk': self.blog.pk})
        self.blogs_url = reverse('bloglistcreateapiview_name')
    
    def generate_test_image_file(self):
        """Helper function to generate a valid image file for testing."""
        image = Image.new('RGB', (100, 100), color = (73, 109, 137))
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)
        return SimpleUploadedFile('test_image.jpg', byte_arr.getvalue(), content_type='image/jpeg')

    def test_bloglistcreateapiview_create(self):
        image = self.generate_test_image_file()
        data = {
            'title': 'New Blog Title',
            'Description': 'New Blog Description',
            'image': image
        }
        response = self.client.post(self.blogs_url, data, format='multipart')
        if response.status_code != status.HTTP_201_CREATED:
            print("Create Blog Error:", response.data)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog_table.objects.count(), 2)
        self.assertEqual(Blog_table.objects.last().title, 'New Blog Title')

    def test_blogdetailapiview_put(self):
        image = self.generate_test_image_file()
        data = {
            'title': 'Updated Blog Title',
            'Description': 'Updated Blog Description',
            'image': image
        }
        response = self.client.put(self.blog_url, data, format='multipart')
        if response.status_code != status.HTTP_200_OK:
            print("Update Blog Error:", response.data)  # Debugging line
        self.blog.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.blog.title, 'Updated Blog Title')

    def test_blogdetailapiview_delete(self):
        """
        Ensure we can delete a blog via the BlogDetailAPIView.
        """
        response = self.client.delete(self.blog_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Blog_table.objects.count(), 0)

    def test_blogdetailapiview_get(self):
        """
        Ensure we can retrieve a blog detail via the BlogDetailAPIView.
        """
        response = self.client.get(self.blog_url)
        blog = Blog_table.objects.get(pk=self.blog.pk)
        serializer = BlogSerializer(blog)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_bloglistcreateapiview_get(self):
        """
        Ensure we can retrieve a list of blogs.
        """
        response = self.client.get(self.blogs_url)
        blogs = Blog_table.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
