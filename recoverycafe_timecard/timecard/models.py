from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Branch(models.Model):
    branch_name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'Branch(%s)' % self.branch_name


class Task(models.Model):
    task_name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'Task(%s)' % self.task_name

class Volunteer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    staff_id = models.IntegerField(unique=True)

    def __unicode__(self):
        return u'User(%s %s)' % (self.first_name, self.last_name)

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
            max_length=8,
            choices = (
                ('IN', 'Punch In'),
                ('OUT', 'Punch Out'),
            )
    )
    punch_time = models.DateTimeField()
    flags = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'PunchTime(%s %s, %s, %s)' % (self.volunteer_id.first_name, self.volunteer_id.last_name, self.get_punch_type_display(), unicode(self.punch_time))
