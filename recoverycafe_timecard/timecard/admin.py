from django.contrib import admin
from .models import Branch, Task, Volunteer, PunchTime

admin.site.register(Branch)
admin.site.register(Task)
admin.site.register(Volunteer)
admin.site.register(PunchTime)
