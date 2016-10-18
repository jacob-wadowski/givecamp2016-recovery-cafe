from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission
from login.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        BLANK_DATA_TEMPLATE_FILE = "timecard/fixtures/initialdatatemplate"
        BLANK_DATA_FILE = BLANK_DATA_TEMPLATE_FILE + u'.json'

        perms = Permission.objects.all()
        authpk = perms.get(codename=SUPERVISION_PERMISSION).pk

        with open(BLANK_DATA_TEMPLATE_FILE) as templateData:
            templateDataStr = templateData.read().replace(u'__authpk__',str(authpk))

        with open(BLANK_DATA_FILE,'w+') as dataFile:
            dataFile.write(templateDataStr)
