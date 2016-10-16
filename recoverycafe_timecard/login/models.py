from __future__ import unicode_literals
from django.db import models

class Login(models.Model):
    class Meta:
	permissions = (
		("supervision_permission", "Can access admin views"),
	)
