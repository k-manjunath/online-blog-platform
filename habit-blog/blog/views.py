#from operator import truediv
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render

from users.models import User

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)

from .models import Post, Habit

#from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home'
    }
    return render(request, 'blog/home.html',context)

class HabitListView(ListView):
    model = Habit
    template_name = 'blog/home.html'
    context_object_name = 'habits'
    ordering = ['-date_created']

class HabitDetailView(DetailView):
    model = Habit

class UserHabitListView(ListView):
    model = Habit
    template_name = 'blog/user_habits.html'
    context_object_name = 'habits'
    #ordering = ['-date_created']   we don't require this anymore as we can override it in get_queryset method by order_by() attr

    #to get data of particular data we need to query kada ra nanna
    '''get_queryset method is overridden here to return habits of a particular user rather than all habit objects,
    We will get username of a user and use that to retrive all habit objects associated with him'''
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        
        return Habit.objects.filter(author=user).order_by('-date_created')

class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    fields = ['title', 'context']

    '''we need to override the form_override method in order to tell django who is actually creating a habit
        asking that in the form doesn't make any sense because a user doesn't want to enter his username everytime he creates/updates a form'''
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class HabitUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Habit
    fields = ['title', 'context']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    '''test_func is the method that UserPassesMixin will run in order to check some condition on user'''
    def test_func(self):
        habit = self.get_object()    #get_object returns the habit that we are currently updating
        if self.request.user == habit.author:
            return True
        return False

class HabitDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Habit
    
    #this is the url that django redirects us to after deleting a object(to home after deleting a habit in this case)
    success_url = '/'

    def test_func(self):
        habit = self.get_object()
        if self.request.user == habit.author:
            return True
        return False

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


'''class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')'''

class PostDetailView(DetailView):
    model = Post


#@login_required <decorators can't be used on classes(only on function based views). WE NEED TO USE MIXINS>
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.habit_id = self.kwargs['pk']
        if form.instance.habit.author == self.request.user:
            form.instance.author = self.request.user
            return super().form_valid(form)
        else:
            return HttpResponseNotAllowed()

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    

def about(request):
    return render(request, 'blog/about.html',{'title':'About'})
