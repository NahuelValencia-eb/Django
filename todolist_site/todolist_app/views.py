from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from .models import Task
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from eventbrite import Eventbrite


# Create your views here.

class Login(LoginView):
    pass


class Logout(LogoutView):
    pass


class TaskList(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'priority']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super(TaskCreate, self).form_valid(form)
    
    def check_task(request, pk):
        task = Task.objects.get(pk=pk)
        if not task.done:
            task.done = True
        task.save()
        return redirect('task-list')


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'priority']
    success_url = reverse_lazy('task-list')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')


class Event(TemplateView):
    template_name = "events_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_event(user):
        social = user.social_auth.filter(provider='eventbrite')[0]
        eb = Eventbrite(social.access_token)
        events = eb.get('/users/me/events/')
        return [event for event in events['events']]
