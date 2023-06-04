from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Group(models.Model):
    header = models.CharField(max_length=200)
    is_subgroup = models.BooleanField(default=False)
    has_subgroup = models.BooleanField(default=False)
    subgroup = models.ManyToManyField('self', null=True)
    users = models.ManyToManyField(User)
class Table(models.Model):
    header = models.CharField(max_length=200)
    participants = models.ManyToManyField(User)
    TableGroup = models.ManyToManyField(Group)
class Task(models.Model):
    task_text = models.CharField(max_length=200)

    task_table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    pub_date = models.DateTimeField("date published", default=timezone.now)