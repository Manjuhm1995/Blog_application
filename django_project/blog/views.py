from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)




# Create your views here.
def home(request):
    context={
        'posting':Post.objects.all()
    }
    return render(request,'blog/home.html',context)
class PostListView(ListView):
    model = Post
    # to change the template we want to use for this view
    template_name = 'blog/home.html'
    # orelse we could create naming convention of the template such as
    # <app>/<model>_<viewtype>.html
    context_object_name = 'posting'
    ordering = ['-date_posted']
    paginate_by = 2

class UserPostListView(ListView):
    model = Post
    # to change the template we want to use for this view
    template_name = 'blog/user_posts.html'
    # orelse we could create naming convention of the template such as
    # <app>/<model>_<viewtype>.html
    context_object_name = 'posting'

    paginate_by = 2
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
#     when we dealing with detail view which expects context of template to be  called object
#     hat,s why we are using object in the detail_view.html instead of post


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView)    :
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user==post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html',{'title':'about'})

