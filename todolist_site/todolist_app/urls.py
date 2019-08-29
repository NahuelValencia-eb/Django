from django.conf.urls import url
from . import views
from todolist_app.views import Login, Event

urlpatterns = [
    url(r'events/(?P<idEvent>[0-9]+)/task/create/', views.TaskCreate.as_view(), name='task-create-event'),
    # url(r'create/$', views.TaskCreate.as_view(), name='task-create'),
    url(r'update/(?P<pk>[0-9]+)/$', views.TaskUpdate.as_view(), name='task-update'),
    url(r'check/(?P<pk>[0-9]+)/$', views.TaskCreate.check_task, name='task-check'),
    url(r'delete/(?P<pk>[0-9]+)/$', views.TaskDelete.as_view(), name='task-delete'),
    #url(r'', views.TaskList.as_view(), name='task-list'),
    url('events/(?P<idEvent>[0-9]+)/tasks', views.TaskList.as_view(), name='event-task-list'),
    url('events/', Event.as_view(), name='events-list'),
]
