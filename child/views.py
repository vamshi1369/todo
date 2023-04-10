from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy 
from child.models import Task
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# we can use the below process as well in order to import the modules

# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

# Create your views here.

class CreateLogin(LoginView):
    template_name = 'child/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todolist')
    
class RegisterPage(FormView):
    template_name = 'child/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todolist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todolist')
        return super(RegisterPage, self).get(*args, **kwargs)

class TodoList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'child/task_list.html' # this is optional if we cannot mention here, then also we can run
    context_object_name = 'tasks' # this is customized and we can mentioned name as our wish to change default one called "object_list"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['color'] = 'red'  # this is just for our understanding and we have to mention {{color}} in task_list.html to fetch the data
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or '' # here we are searching the keyword or empty string to filter 
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        
        context['search_input'] = search_input

        return context

class TodoDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task' # this is customized and we can mentioned name as our wish to change default one called "object"
    template_name = 'child/task_detail.html' # we can change the html name as well by changing in the template folder like 'task.html' instead 'task_detail.html'


class TodoCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'child/task_form.html' # here it redirects to task_form.html by default even thought if we haven't mentioned as well.
    fields = ['title', 'description', 'complete'] # here we can also give like ['title', 'description', 'complete', 'create'] or '__all__'
    success_url = reverse_lazy('todolist') # here it will again redirect to home page and ignore any error messages like 'Reverse Not Found'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate, self).form_valid(form)

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'child/task_form.html' # here it redirects to task_form.html by default even thought if we haven't mentioned as well.
    fields = ['title', 'description', 'complete'] # here we can also give like '__all__' then we will getting the extract field like 'user' as well
    success_url = reverse_lazy('todolist')

class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'child/task_confirm_delete.html' # here it redirects to task_form.html by default even thought if we haven't mentioned as well.
    context_object_name = 'tesk'
    success_url = reverse_lazy('todolist')
