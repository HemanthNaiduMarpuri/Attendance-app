from django.contrib import admin
from .models import Batch, Semester, Section, Semester_Subject, Subject

# Register your models here.
admin.site.register(Batch)
admin.site.register(Semester)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(Semester_Subject)