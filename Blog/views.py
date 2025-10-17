from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, authenticate, get_user_model
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
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


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

def about(request):
    return render(request, 'Blog/about.html')

# below AboutTemplateView and AboutView are the equivalent cbv for about() fbv
class AboutTemplateView(TemplateView):
    template_name = 'Blog/about.html'

class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Blog/about.html')

def contact(request):
    return render(request, 'Blog/contact.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


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


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!! You have become an Author.')
            return HttpResponseRedirect('/dashboard/')
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

def blog_update(request, id):
    context = {}
    try:
        blog_obj = Blog_table.objects.get(pk=id)
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


def delete_blog(request, id):
    if request.user.is_authenticated:
        pi = Blog_table.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

# below DeleteBlogView is equivalent cbv for delete_blog() fbv
class DeleteBlogView(LoginRequiredMixin, View):
    def get(self, request, id):
        blog = Blog_table.objects.get(pk=id)
        blog.delete()
        return redirect('dashboard_name')  # Assuming 'dashboard_name' is the name of your dashboard URL

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

    class CustomPageNumberPagination(PageNumberPagination):
        # default page size when user doesn't pass `page_size`
        page_size = 10
        # allow client to set the page size using `page_size` query param
        page_size_query_param = 'page_size'
        # limit maximum page size to prevent abuse
        max_page_size = 100
        # the query param name for the page number
        page_query_param = 'page'

        def get_paginated_response(self, data):
            """Return a Response with pagination metadata including total pages.

            This implementation is defensive: it attempts to read paginator attributes
            but falls back gracefully if something is missing.
            """
            # defaults
            total_pages = None
            current_page = None
            effective_page_size = self.page_size

            # Try to read values from the paginator/page
            if hasattr(self, 'page') and self.page is not None:
                paginator = getattr(self.page, 'paginator', None)
                if paginator is not None:
                    total_count = getattr(paginator, 'count', None)
                    per_page = getattr(paginator, 'per_page', None)
                    if per_page:
                        effective_page_size = per_page
                    if total_count is not None and effective_page_size:
                        try:
                            total_pages = (total_count + effective_page_size - 1) // effective_page_size
                        except Exception:
                            total_pages = None
                current_page = getattr(self.page, 'number', None)

            # honor client-provided page_size if set
            try:
                client_page_size = self.get_page_size(self.request)
                if client_page_size:
                    effective_page_size = client_page_size
            except Exception:
                pass

            return Response({
                'count': getattr(getattr(self, 'page', None), 'paginator', None) and getattr(self.page.paginator, 'count', None),
                'total_pages': total_pages,
                'page': current_page,
                'page_size': effective_page_size,
                # how many items are in this response (current page length)
                'results_count': len(data) if data is not None else 0,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
            })

    def get(self, request):
        """List blogs with optional filtering and page number pagination.

        Supported query params:
          - page (int): page number (default 1)
          - page_size (int): items per page (default 10, max 100)
          - q (str): full-text search against title and Description
          - title (str): filter by title contains
          - author (str): filter by author's username or email (exact match)
          - ordering (str): Django ordering string (e.g. `-id` or `title`)
        """
        qs = Blog_table.objects.all()

        q = request.query_params.get('q')
        title = request.query_params.get('title')
        author = request.query_params.get('author')
        ordering = request.query_params.get('ordering')

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(Description__icontains=q))

        if title:
            qs = qs.filter(title__icontains=title)

        if author:
            # try matching against username or email on the related user
            qs = qs.filter(Q(user_id__username__iexact=author) | Q(user_id__email__iexact=author))

        if ordering:
            try:
                qs = qs.order_by(ordering)
            except Exception:
                # ignore invalid ordering and fall back to default
                pass

        paginator = self.CustomPageNumberPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        serializer = BlogSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

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


class UserTokenObtainPairAPIView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if user := authenticate(username=email, password=password):
            refresh_token = RefreshToken.for_user(user)
            access_token = AccessToken.for_user(user)
            return Response(data={  "email": email,
                                    "access_token": str(access_token),
                                    "refresh_token": str(refresh_token)
                                    }, status=status.HTTP_200_OK)
        else:
            return Response(data={'status': "Invalid Credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)


class SignupAPIView(APIView):
    """API view to register a new user using email as username.

    Expected payload (JSON):
      - email (required)
      - password or password1 (required)
      - password2 (optional; if provided, must match password1)
      - first_name (optional)
      - last_name (optional)

    Responses:
      201: user created
      400: validation errors
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = (data.get('email') or '').strip()
        password1 = data.get('password1') or data.get('password')
        password2 = data.get('password2') or password1
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        errors = {}
        if not email:
            errors['email'] = 'This field is required.'
        if not password1:
            errors['password'] = 'This field is required.'
        if password1 and password2 and password1 != password2:
            errors['password2'] = "Passwords do not match."

        UserModel = get_user_model()
        if email and (UserModel.objects.filter(email=email).exists() or UserModel.objects.filter(username=email).exists()):
            errors['email'] = 'User with this email already exists.'

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # create the user
        try:
            user = UserModel.objects.create_user(
                username=email,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'user created', 'email': user.email}, status=status.HTTP_201_CREATED)
