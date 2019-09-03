from django.conf import settings
from django.db import models


# Create your models here.
class Priority(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Task(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None
    )
    done = models.BooleanField(default=False)
    id_event = models.IntegerField(default=None)
