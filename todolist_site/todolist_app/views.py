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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task-list'] = Task.objects.filter(idEvent=self.kwargs['idEvent'])
        context['idEvent'] = self.kwargs['idEvent']
        return context

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user, idEvent=self.kwargs['idEvent'])


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'priority']
    success_url = reverse_lazy('events-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.idEvent = self.kwargs['idEvent']
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
    model = Task
    template_name = "events_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = self.get_event()
        return context

    def get_event(self):
        social = self.request.user.social_auth.filter(provider='eventbrite')[0]
        eb = Eventbrite(social.access_token)
        events = eb.get('/users/me/events/')
        # [event for event in events['events']]
        return events
