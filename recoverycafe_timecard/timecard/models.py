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
    active = models.BooleanField(default=True)

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
    punch_time = models.DateTimeField(auto_now_add=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    isAdminCheckout = models.NullBooleanField()
    adminCheckoutTime = models.DateTimeField(max_length=50, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if kwargs.get('overrideTime'):
            self.punch_time = kwargs.pop('overrideTime', False)
        super(PunchTime, self).save(*args, **kwargs)


    def __unicode__(self):
        return u'PunchTime(%s %s, %s, %s)' % (self.volunteer_id.first_name, self.volunteer_id.last_name, self.get_punch_type_display(), unicode(self.punch_time))

class Report(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    staff_id = models.IntegerField()
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    branch_name = models.CharField(max_length=64)
    task_name = models.CharField(max_length=64)
    punch_time_in = models.DateTimeField()
    punch_time_out = models.DateTimeField()
    session_time_hours = models.FloatField()

    class Meta:
        managed = False
        db_table = 'view_report'

    def save(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

class LastKnownStatus(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    staff_id = models.IntegerField()
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    punch_time_latest = models.DateTimeField()
    punch_type_latest = models.CharField(
            max_length=8,
            choices = (
                ('IN', 'Punch In'),
                ('OUT', 'Punch Out'),
            )
    )

    class Meta:
        managed = False
        db_table = 'view_last_known_status'

    def save(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass