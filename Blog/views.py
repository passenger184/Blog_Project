from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

# Create your views here.



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'home.html'   #by default it will look <apps>/<model>_<listview>.html
    context_object_name = 'posts'  #by default django calls it object but we want to call is posts
    ordering = ['-date_posted']   #to liist from newest to oldest
    paginate_by = 4


class UserPostListView(ListView):  #all posts by specific user
    model = Post
    template_name = 'allposts.html'   
    context_object_name = 'posts'  
    paginate_by = 4
    
    def get_queryset(self):  #get the user and all posts by him only and if user not exist return 404
        user = get_object_or_404(User, username=self.kwargs.get('username')) #get username from route kwargs is used for this
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'
    
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'create.html'    
    
    def form_valid(self, form):   #to tell the author
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'create.html'    
    
    def form_valid(self, form):   #to tell the author
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = Post
    template_name = 'delete.html'  
    success_url = '/'
      
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    
        
        
        

def about(request):
    context = {}
    return render(request, 'about.html', context)
