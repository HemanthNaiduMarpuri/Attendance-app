from django.urls import path
from .views import student_timetable, mark_attendance, mark_holiday, semester_calendar, attendance_percentage

urlpatterns = [
    path('timetable/', student_timetable, name='timetable'),
    path('timetable/mark_attendance/<int:timetable_id>/', mark_attendance, name='mark_attendance'),
    path('timetable/mark_holiday/', mark_holiday, name='mark_holiday'),
    path('timetable/calendar/', semester_calendar, name='semester_calendar'),
    path('timetable/attendance-percentage/', attendance_percentage, name='attendance_percentage')
]
