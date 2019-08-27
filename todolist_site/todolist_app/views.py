from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Task
from django.urls import reverse_lazy
from django.shortcuts import redirect


# Create your views here.

class Login(LoginView):
    pass


class Logout(LogoutView):
    pass


class TaskList(ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)


class TaskCreate(CreateView):
    model = Task
    fields = ['name', 'priority']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    fields = ['name', 'priority']
    success_url = reverse_lazy('task-list')


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')


def check_task(request, pk):
    task = Task.objects.get(pk=pk)
    if not task.done:
        task.done = True
    task.save()
    return redirect('task-list')