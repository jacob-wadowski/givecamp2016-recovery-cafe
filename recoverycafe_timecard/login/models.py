from __future__ import unicode_literals
from django.db import models

SUPERVISION_PERMISSION = u'supervision_permission'
FULL_SUPERVISION_PERMISSION = u'login.' + SUPERVISION_PERMISSION

class Login(models.Model):
    class Meta:
        permissions = (
            (SUPERVISION_PERMISSION, "Can access admin views"),
        )
