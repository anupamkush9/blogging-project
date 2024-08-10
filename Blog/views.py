from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from .models import Blog_table
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import Group
from django.contrib.auth import login as auth_login
from .forms import BlogForm
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from rest_framework import viewsets
from .serializers import BlogSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication


def home(request):
    context = {'blogs': Blog_table.objects.all()}
    return render(request, 'Blog/home.html', context)

# below HomeGenericView and HomeView are the equivalent cbv for home() fbv
class HomeListView(ListView):
    model = Blog_table
    template_name = 'Blog/home.html'
    context_object_name = 'blogs'

class HomeView(View):
    def get(self, request):
        blogs = Blog_table.objects.all()
        context = {'blogs': blogs}
        return render(request, 'Blog/home.html', context)


def blog_detail(request, id):
    blog = Blog_table.objects.get(id=id)
    return render(request, 'Blog/blog_detail.html', {'blog': blog})

# below BlogDetailView and BlogDetailDetailView are the equivalent cbv for blog_detail() fbv
class BlogDetailView(View):
    def get(self, request, id):
        blog = get_object_or_404(Blog_table, id=id)
        return render(request, 'Blog/blog_detail.html', {'blog': blog})

class BlogDetailDetailView(DetailView):
    model = Blog_table
    template_name = 'Blog/blog_detail.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'id'
# about


def about(request):
    return render(request, 'Blog/about.html')

# below AboutTemplateView and AboutView are the equivalent cbv for about() fbv
class AboutTemplateView(TemplateView):
    template_name = 'Blog/about.html'

class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Blog/about.html')
# Contact


def contact(request):
    return render(request, 'Blog/contact.html')


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# login view


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/')
        else:
            form = LoginForm()
        return render(request, 'Blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


# Sigup
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations!! You have become an Author.')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'Blog/signup.html', {'form': form})


def dashboard(request):
    if request.user.is_authenticated:
        blogs = Blog_table.objects.filter(user_id=request.user.id)
        full_name = request.user.username
        gps = request.user.groups.all()
        return render(request, 'Blog/dashboard.html', {'blogs': blogs, 'full_name': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')

# below DashboardView and DashboardTemplateView are the equivalent cbv for dashboard() fbv
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            blogs = Blog_table.objects.filter(user_id=request.user.id)
            full_name = request.user.username
            gps = request.user.groups.all()
            context = {
                'blogs': blogs,
                'full_name': full_name,
                'groups': gps,
            }
            return render(request, 'Blog/dashboard.html', context)
        else:
            return HttpResponseRedirect('/login/')

class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'Blog/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog_table.objects.filter(user_id=self.request.user.id)
        context['full_name'] = self.request.user.username
        context['groups'] = self.request.user.groups.all()
        return context        

# Add New Post
def add_blog(request):
    context = {'form': BlogForm()}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user
            # print(request.POST.get['Description'])
            if form.is_valid():
                Description = form.cleaned_data['Description']
            blog_obj = Blog_table.objects.create(
                user_id=user, title=title, Description=Description, image=image)
            messages.success(request, 'Blog has been added successfully.')
            print(blog_obj)
            return redirect('/add_blog/')
    except Exception as e:
        print(e)
    return render(request, 'Blog/add_blog.html', context)

# update it


def blog_update(request, id):
    context = {}
    try:
        blog_obj = Blog_table.objects.get(pk=id)
        print("------------------------->")
        print(blog_obj.image)
        if blog_obj.user_id != request.user:

            return redirect('/')
        initial_dict = {'Description': blog_obj.Description}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']

            title = request.POST.get('title')
            user = request.user
            if form.is_valid():
                Description = form.cleaned_data['Description']
            blog_obj = Blog_table.objects.create(
                user_id=user, title=title, Description=Description, image=image)
            messages.success(request, 'Blog has been updated successfully.')
        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)
    return render(request, 'Blog/blog_update.html', context)

# Delete Post


def delete_blog(request, id):
    if request.user.is_authenticated:
        print("request is authenticated........")
    # if request.method == 'POST':
        print("dashboard wala blog is running............")
        pi = Blog_table.objects.get(pk=id)
        print("fetching is done bhai...........")
        pi.delete()
        print("deletion is also done........")
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

# below DeleteBlogView is equivalent cbv for delete_blog() fbv
class DeleteBlogView(LoginRequiredMixin, View):
    def get(self, request, id):
        blog = Blog_table.objects.get(pk=id)
        blog.delete()
        return redirect('dashboard')  # Assuming 'dashboard' is the name of your dashboard URL

########################################## API  CODE Implemenation #######################################################
class BlogViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Blog_table.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class BlogListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = Blog_table.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # blog = Blog_table.objects.get(pk=pk)
        blog = get_object_or_404(Blog_table, pk=pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

	# 1st argument represents the instance of the Blog_table model that we want to update. and 2nd argument is the new data that we want to apply to the instance.
    def put(self, request, pk):
        # blog = Blog_table.objects.get(pk=pk)
        blog = get_object_or_404(Blog_table, pk=pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        blog = get_object_or_404(Blog_table, pk=pk)
        serializer = BlogSerializer(blog, data=request.data, partial=True)  # Set partial=True for partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # blog = Blog_table.objects.get(pk=pk)
        blog = get_object_or_404(Blog_table, pk=pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
