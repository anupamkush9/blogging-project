from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Blog import views

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home_name')
        self.assertEqual(resolve(url).func, views.home)

    def test_homeview_url_is_resolved(self):
        url = reverse('homeview_name')
        self.assertEqual(resolve(url).func.view_class, views.HomeView)

    def test_homelistview_url_is_resolved(self):
        url = reverse('homelistview_name')
        self.assertEqual(resolve(url).func.view_class, views.HomeListView)

    def test_blog_detail_url_is_resolved(self):
        url = reverse('blog_detail_name', args=[1])
        self.assertEqual(resolve(url).func, views.blog_detail)

    def test_blogdetailview_url_is_resolved(self):
        url = reverse('blogdetailview_name', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.BlogDetailView)

    def test_blogdetaildetailview_url_is_resolved(self):
        url = reverse('blogdetaildetailview_name', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.BlogDetailDetailView)

    def test_add_blog_url_is_resolved(self):
        url = reverse('add_blog_name')
        self.assertEqual(resolve(url).func, views.add_blog)

    def test_about_url_is_resolved(self):
        url = reverse('about_name')
        self.assertEqual(resolve(url).func, views.about)

    def test_abouttemplateview_url_is_resolved(self):
        url = reverse('abouttemplateview_name')
        self.assertEqual(resolve(url).func.view_class, views.AboutTemplateView)

    def test_aboutview_url_is_resolved(self):
        url = reverse('aboutview_name')
        self.assertEqual(resolve(url).func.view_class, views.AboutView)

    def test_dashboard_url_is_resolved(self):
        url = reverse('dashboard_name')
        self.assertEqual(resolve(url).func, views.dashboard)

    def test_dashboardview_url_is_resolved(self):
        url = reverse('dashboardview_name')
        self.assertEqual(resolve(url).func.view_class, views.DashboardView)

    def test_dashboardtemplateview_url_is_resolved(self):
        url = reverse('dashboardtemplateview_name')
        self.assertEqual(resolve(url).func.view_class, views.DashboardTemplateView)

    def test_delete_blog_url_is_resolved(self):
        url = reverse('delete_blog_name', args=[1])
        self.assertEqual(resolve(url).func, views.delete_blog)

    def test_deleteblogview_url_is_resolved(self):
        url = reverse('deleteblogview_name', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.DeleteBlogView)

    def test_contact_url_is_resolved(self):
        url = reverse('contact_name')
        self.assertEqual(resolve(url).func, views.contact)

    def test_login_url_is_resolved(self):
        url = reverse('login_name')
        self.assertEqual(resolve(url).func, views.login)

    def test_logout_url_is_resolved(self):
        url = reverse('logout_name')
        self.assertEqual(resolve(url).func, views.user_logout)

    def test_signup_url_is_resolved(self):
        url = reverse('signup_name')
        self.assertEqual(resolve(url).func, views.signup)

    def test_blog_update_url_is_resolved(self):
        url = reverse('blog_update_name', args=[1])
        self.assertEqual(resolve(url).func, views.blog_update)

    def test_bloglistcreateapiview_url_is_resolved(self):
        url = reverse('bloglistcreateapiview_name')
        self.assertEqual(resolve(url).func.view_class, views.BlogListCreateAPIView)

    def test_blogdetailapiview_url_is_resolved(self):
        url = reverse('blogdetailapiview_name', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.BlogDetailAPIView)
