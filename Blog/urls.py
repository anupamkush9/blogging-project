from django.urls import path
from Blog import views
urlpatterns = [
    path('',views.home,name='home'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('blog_detail/<int:id>',views.blog_detail,name='blog_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete_blog/<int:id>/', views.delete_blog, name='delete_blog'),
    path('blog_update/<int:id>/' , views.blog_update , name="blog_update"),
]
