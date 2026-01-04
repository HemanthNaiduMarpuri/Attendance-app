from django.db import models
from academics.models import Section, Subject, Semester

SESSION_TYPE_CHOICES = (
    ('Theory', 'Theory'),
    ('Lab', 'Lab')
)

DAY_CHOICES = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
)

class Period(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='sem_period')
    period_number = models.PositiveIntegerField(unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.period_number} -> ({self.start_time} - {self.end_time})"
    
class TimeTable(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_timetable')
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='batch_timetable')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='section_subject')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default="Theory")
    span_count = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.day} -> {self.period} -> {self.subject}"