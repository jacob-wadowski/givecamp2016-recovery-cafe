from __future__ import unicode_literals
from django.db import models

SUPERVISIONPERMISSION = u'login.supervision_permission'

class Login(models.Model):
    class Meta:
        permissions = (
            (SUPERVISIONPERMISSION, "Can access admin views"),
        )
