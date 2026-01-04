from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord, Holiday

admin.site.register(AttendanceSession)
admin.site.register(AttendanceRecord)
admin.site.register(Holiday)
