from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.base import TemplateView, RedirectView
from blog.forms import PostForm
from blog.models import Post
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

# Create your views here.

# FUNCTION BASE VIEW
# def indexView(request):
#     """
#     a view for function based to show index page
#     """
#     name = 'ali'
#     context = {
#         "name": name
#     }
#     return render(request, 'index.html',context)


# creating manually this class base view with extra features
class IndexView(TemplateView):
    """
    a class base view for showing index page
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        context["post"] = Post.objects.all()
        return context


class RedirectToMaktab(RedirectView):
    url = "https://maktabkhoone.com"

    # def get_redirect_url(self, *args, **kwargs):


class PostList(LoginRequiredMixin, ListView):
    ## 3 are same
    # queryset = Post.objects.all()
    login_url = "/blog/post/"
    model = Post
    context_object_name = "posts"
    paginate_by = 3
    ordering = "id"

    ## in baraye customize kardan
    # def get_queryset(self):
    #     posts = Post.objects.filter(status=False)
    #     return posts


class PostDetailView( LoginRequiredMixin, DetailView):

    model = Post

# class PostCreateView(FormView):
#     template_name = 'contact.html'
#     form_class = PostForm
#     success_url = '/blog/post/'
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "status", "category", "published_date"]
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/post/"
