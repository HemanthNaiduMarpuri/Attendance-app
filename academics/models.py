from django.db import models


SEMESTER_CHOICES = (
    ('1-1', '1-1'),
    ('1-2', '1-2'),
    ('2-1', '2-1'),
    ('2-2', '2-2'),
    ('3-1', '3-1'),
    ('3-2', '3-2'),
    ('4-1', '4-1'),
    ('4-2', '4-2')
)

SUBJECT_TYPE_CHOICES = (
    ('Theory', 'Theory'),
    ('Practical-Lab', 'Practical-Lab')
)

STATUS_CHOICES = (
    ('Active', 'Active'),
    ('InActive', 'InActive')
)

class Batch(models.Model):
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self):
        return f"{self.start_year}-{self.end_year}"
    
class Semester(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sem_batch')
    semester = models.CharField(max_length=15, choices=SEMESTER_CHOICES, default='1-1')
    semester_start_date = models.DateField()
    semester_end_date = models.DateField()

    def get_months(self):
        current = self.semester_start_date
        months = []

        while current <= self.semester_end_date:
            months.append((current.year, current.month))

            if current.month == 12:
                current = current.replace(year=current.year +1, month=1, day=1)
            else:
                current = current.replace(month=current.month+1, day=1)
        return months
    
    def __str__(self):
        return f"{self.semester} - ({self.semester_start_date} - {self.semester_end_date})"
    
class Subject(models.Model):
    subject_code = models.CharField(max_length=50, unique=True)
    subject_name = models.CharField(max_length=100)
    subject_type = models.CharField(max_length=30, choices=SUBJECT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.subject_name} -> {self.subject_type}"

class Semester_Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='sem_year')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sem_subject')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('semester', 'subject')

    def __str__(self):
        return f"{self.semester} -> {self.subject}"
    
class Section(models.Model):
    department_name = models.CharField(max_length=255)
    section = models.CharField(max_length=10)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_section')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='section_sem')

    def __str__(self):
        return f"{self.department_name} -> {self.section} -> {self.batch} -> {self.semester}"


