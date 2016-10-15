from __future__ import unicode_literals

from django.db import models

class Branch(models.Model):
    branch_name = models.CharField(max_length=64)

class Task(models.Model):
    task_name = models.CharField(max_length=64)

class Volunteer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    staff_id = models.IntegerField(unique=True)

class PunchTime(models.Model):
    volunteer_id = models.ForeignKey(
            Volunteer,
            on_delete=models.CASCADE
    )
    task_id = models.ForeignKey(
            Task,
            on_delete=models.CASCADE
    )
    branch_id = models.ForeignKey(
            Branch,
            on_delete=models.CASCADE
    )
    punch_type = models.CharField(
            max_length=64,
            choices = (
                ('IN', 'Punch In'),
                ('OUT', 'Punch Out'),
            )
    )
    punch_time = models.DateTimeField()
    flags = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)
