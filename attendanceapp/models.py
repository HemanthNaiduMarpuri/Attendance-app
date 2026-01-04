from django.db import models
from accounts.models import Student
from academics.models import Section
from timetable.models import TimeTable

STATUS_CHOICES = (
    ('Present', 'Present'),
    ('Absent', 'Absent'),
    ('Leave', 'Leave')
)

class AttendanceSession(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='attend_session')
    time_table = models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='attend_timetable')
    date = models.DateField()

    def __str__(self):
        return f"{self.section} -> {self.time_table} -> {self.date}"

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance')
    attendance_session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='student_attended_session')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} -> {self.attendance_session} -> {self.status}"

class Holiday(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='holiday_section')
    date = models.DateField()
    created_by = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('section', 'date')

    def __str__(self):
        return f"{self.section} -> {self.date} -> {self.created_by}"

