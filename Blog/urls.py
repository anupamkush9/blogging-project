from django.urls import path, include
from Blog import views
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)

urlpatterns = [

    path('home/',views.home,name='home_name'),
    # below are the 2 class based view implementation for this function based view
    path('', views.HomeView.as_view(), name='homeview_name'),
    path('homegenericview', views.HomeListView.as_view(), name='homelistview_name'),

    path('blog_detail/<int:id>/', views.blog_detail, name='blog_detail_name'),
    # below are the 2 class based view implementation for this function based view
    path('blogdetailview/<int:id>/', views.BlogDetailView.as_view(), name='blogdetailview_name'),
    path('blogdetaildetailview/<int:id>/', views.BlogDetailDetailView.as_view(), name='blogdetaildetailview_name'),
    
    path('add_blog/', views.add_blog, name='add_blog_name'),
    
    path('about/', views.about, name='about_name'),
    # below are the 2 class based view implementation for this function based view
    path('abouttemplateview/', views.AboutTemplateView.as_view(), name='abouttemplateview_name'),
    path('aboutview/', views.AboutView.as_view(), name='aboutview_name'),

    path('dashboard/', views.dashboard, name='dashboard_name'),
    # below are the 2 class based view implementation for this function based view
    path('dashboardview/', views.DashboardView.as_view(), name='dashboardview_name'),
    path('dashboardtemplateview/', views.DashboardTemplateView.as_view(), name='dashboardtemplateview_name'),

    path('delete_blog/<int:id>/', views.delete_blog, name='delete_blog_name'),
    # below are the 2 class based view implementation for this function based view
    path('DeleteBlogView/<int:id>/', views.DeleteBlogView.as_view(), name='deleteblogview_name'),
   
    path('contact/', views.contact, name='contact_name'),
    path('login/', views.login, name='login_name'),
    path('logout/', views.user_logout, name='logout_name'),
    path('signup/', views.signup, name='signup_name'),
    path('blog_update/<int:id>/' , views.blog_update , name="blog_update_name"),
    
    # route for apis
    path('api/v1/', include(router.urls)),
    
    path('api/blogs/', views.BlogListCreateAPIView.as_view(), name="bloglistcreateapiview_name"),  # For list and create
    path('api/blogs/<int:pk>/', views.BlogDetailAPIView.as_view(), name="blogdetailapiview_name"),  # For retrieve, update, and delete

]
