from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from .models import Blog_table
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import Group
from django.contrib.auth import login as auth_login
from .forms import BlogForm
# Create your views here.


def home(request):
    context = {'blogs': Blog_table.objects.all()}
    return render(request, 'Blog/home.html', context)


def blog_detail(request, id):
    blog = Blog_table.objects.get(id=id)
    return render(request, 'Blog/blog_detail.html', {'blog': blog})

# about


def about(request):
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
    return render(request, 'blog/signup.html', {'form': form})


def dashboard(request):
    if request.user.is_authenticated:
        blogs = Blog_table.objects.filter(user_id=request.user.id)
        full_name = request.user.username
        gps = request.user.groups.all()
        return render(request, 'Blog/dashboard.html', {'blogs': blogs, 'full_name': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')


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
