from django.urls import path, include
from Blog import views
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)

urlpatterns = [

    # below are the 2 class based view implementation for function based view
    path('home/',views.home,name='home'),
    path('', views.HomeView.as_view(), name='HomeView'),
    path('homegenericview', views.HomeListView.as_view(), name='HomeGenericView'),

    path('blog_detail/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blogdetailview/<int:id>/', views.BlogDetailView.as_view(), name='BlogDetailView'),
    path('blogdetaildetailview/<int:id>/', views.BlogDetailDetailView.as_view(), name='BlogDetailDetailView'),
    
    path('add_blog/', views.add_blog, name='add_blog'),
    
    path('about/', views.about, name='about'),
    path('abouttemplateview/', views.AboutTemplateView.as_view(), name='about'),
    path('aboutview/', views.AboutView.as_view(), name='about'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboardview/', views.DashboardView.as_view(), name='DashboardView'),
    path('dashboardtemplateview/', views.DashboardTemplateView.as_view(), name='DashboardTemplateView'),

    path('delete_blog/<int:id>/', views.delete_blog, name='delete_blog'),
    path('DeleteBlogView/<int:id>/', views.DeleteBlogView.as_view(), name='DeleteBlogView'),
   
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('blog_update/<int:id>/' , views.blog_update , name="blog_update"),
    
    # route for apis
    path('api/v1/', include(router.urls)),
    

]
