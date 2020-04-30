from django.shortcuts import render
from django.urls import reverse
from .forms import BlogForm, BlogPostForm
from .models import Blog, BlogPost
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView
from django.views import View
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

class NewBlogView(CreateView):
    form_class = BlogForm
    template_name = "blog_settings.html"

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.owner = self.request.user
        blog_obj.slug = slugify(blog_obj.title)

        blog_obj.save()
        return HttpResponseRedirect(reverse('home'))

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if Blog.objects.filter(owner= user).exists():
            return HttpResponseForbidden("You can not create more than one blogs per account")
        else:
            return super(NewBlogView, self).dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            if Blog.objects.filter(owner=self.request.user).exists():
                context["has_blog"] = True
                blog = Blog.objects.get(owner=self.request.user)
                context['blog'] = blog
                context['blog_posts'] = BlogPost.objects.filter(blog=blog)
                context['shared_posts'] = blog.shared_posts.all()

        return context
    


class UpdateBlogView(UpdateView):
    form_class = BlogForm
    template_name = "blog_settings.html"
    success_url = '/'
    model = Blog

    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        objects = super().get_queryset()
        return objects.filter(owner = self.request.user)


class BlogPostView(CreateView):
    form_class = BlogPostForm
    template_name = "blog_post.html"

    def form_valid(self, form):
        blogpost_obj = form.save(commit=False)
        blogpost_obj.blog = Blog.objects.get(owner=self.request.user)
        blogpost_obj.slug = slugify(blogpost_obj.title)
        blogpost_obj.is_published = True
        
        blogpost_obj.save()

        return HttpResponseRedirect(reverse('home'))

    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

class BlogPostUpdateView(UpdateView):
    form_class = BlogPostForm
    template_name = "blog_post.html"
    model = BlogPost
    success_url = '/'

    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        objects = super().get_queryset()
        return objects.filter(blog__owner = self.request.user)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog_post_detail.html"


class ShareBlogPostView(TemplateView):
    template_name = "share_blog_post.html"

    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, pk, **kwargs):
        blog_post = BlogPost.objects.get(pk=pk)
        currently_shared_with = blog_post.shared_to.all()
        currently_shared_with_ids = map(lambda x: x.pk, currently_shared_with)

        exclude_from_can_share_with = [blog_post.blog.pk] + list(currently_shared_with_ids)

        can_be_shared_with = Blog.objects.exclude(pk__in = exclude_from_can_share_with)

        return {
            'post': blog_post,
            'is_shared_with' : currently_shared_with,
            'can_be_shared_with' : can_be_shared_with,
        }


class SharePostWithBlog(View):
    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, post_pk, blog_pk):
        blog_post = BlogPost.objects.get(pk=post_pk)
        if blog_post.blog.owner != request.user:
            return HttpResponseForbidden("You can only share posts that you created.")
        
        blog = Blog.objects.get(pk=blog_pk)
        blog_post.shared_to.add(blog)

        return HttpResponseRedirect(reverse('home'))


class StopSharingPostWithBlog(View):
    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, post_pk, blog_pk):
        blog_post = BlogPost.objects.get(pk = post_pk)
        if blog_post.blog.owner != request.user:
            return HttpResponseForbidden("You can only stop sharing posts that you created.")
        
        blog = Blog.objects.get(pk = blog_pk)
        blog_post.shared_to.remove(blog)
        return HttpResponseRedirect(reverse('home'))




