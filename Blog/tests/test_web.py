from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Blog.models import Blog_table

User = get_user_model()

class BlogViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client.login(username='testuser@gmail.com', password='testpassword')

        self.blog = Blog_table.objects.create(
            user_id=self.user,
            title='Test Blog',
            Description='Test Blog Description'
        )

    ### Function-Based Views (FBVs) ###

    def test_home_view(self):
        response = self.client.get(reverse('home_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/home.html')

    def test_blog_detail_view(self):
        response = self.client.get(reverse('blog_detail_name', args=[self.blog.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/blog_detail.html')

    def test_about_view(self):
        response = self.client.get(reverse('about_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/about.html')

    def test_contact_view(self):
        response = self.client.get(reverse('contact_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/contact.html')

    def test_user_logout_view(self):
        response = self.client.get(reverse('logout_name'))
        self.assertEqual(response.status_code, 302)  # Redirects to login or home after logout

    def test_login_view(self):
        # Instead of assertTemplateUsed, we test if it redirects for authenticated users.
        self.client.logout()  # First, log out to check the login page
        response = self.client.get(reverse('login_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/login.html')

    def test_signup_view(self):
        response = self.client.get(reverse('signup_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/signup.html')

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/dashboard.html')

    def test_add_blog_view(self):
        response = self.client.get(reverse('add_blog_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/add_blog.html')

    def test_blog_update_view(self):
        response = self.client.get(reverse('blog_update_name', args=[self.blog.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/blog_update.html')

    def test_delete_blog_view(self):
        response = self.client.get(reverse('delete_blog_name', args=[self.blog.pk]))
        self.assertEqual(response.status_code, 302)  # Assuming delete redirects after deletion
        self.assertFalse(Blog_table.objects.filter(id=self.blog.pk).exists())

    ### Class-Based Views (CBVs) ###

    def test_homeview_view(self):
        response = self.client.get(reverse('homeview_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/home.html')

    def test_homelistview_view(self):
        response = self.client.get(reverse('homelistview_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/home.html')

    def test_blogdetailview_view(self):
        response = self.client.get(reverse('blogdetailview_name', args=[self.blog.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/blog_detail.html')

    def test_blogdetaildetailview_view(self):
        response = self.client.get(reverse('blogdetaildetailview_name', args=[self.blog.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/blog_detail.html')

    def test_abouttemplateview_view(self):
        response = self.client.get(reverse('abouttemplateview_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/about.html')

    def test_aboutview_view(self):
        response = self.client.get(reverse('aboutview_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/about.html')

    def test_dashboardview_view(self):
        response = self.client.get(reverse('dashboardview_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/dashboard.html')

    def test_dashboardtemplateview_view(self):
        response = self.client.get(reverse('dashboardtemplateview_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/dashboard.html')

    def test_deleteblogview_view(self):
        response = self.client.get(reverse('deleteblogview_name', args=[self.blog.pk]))
        self.assertEqual(response.status_code, 302)  # Assuming delete redirects after deletion
        self.assertFalse(Blog_table.objects.filter(id=self.blog.pk).exists())
